from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.utils import timezone
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework import  views
from rest_framework.response import Response
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from wkhtmltopdf.views import PDFTemplateResponse
from decimal import Decimal

from .models import Payment, Plan, Token, PaymentPlan, PromoCode
from users.models import Membership, MembershipType
from .parsers import XMLParser
from .pantheon import create_move
from home.email_utils import send_email
from .forms import PromoCodeForm
from .utils import get_invoice_number, finish_payment

# Create your views here.

# payments
class PaymentPreview(views.APIView):
    def get(self, request):
        plan_id = request.GET.get('plan_id', False)
        purchase_type = request.GET.get('purchase_type', '')
        plan = Plan.objects.filter(id=plan_id).first()
        user = request.user

        if plan and user:
            payment = Payment(
                user=user,
            )
            payment.user_was_eligible_to_discount = user.is_eligible_to_discount()
            price = plan.discounted_price if payment.user_was_eligible_to_discount else plan.price
            payment.amount = price
            payment.save()
            PaymentPlan(plan=plan, payment=payment, price=price, plan_name=plan.name).save()

            if plan.item_type.name == 'uporabnina':
                # if plan is uporabnina add clanarina to payment
                membership = user.membership

                # check if user has active membership for entire duration of new uporabnina
                last_payment_plan = user.payments.get_last_active_subscription_payment_plan()
                valid_to = last_payment_plan.valid_to if last_payment_plan and last_payment_plan.valid_to else timezone.now()
                new_uporabnina_valid_to = valid_to + timedelta(days=plan.duration)
                last_active_membership = user.get_last_active_membership()
                if (not last_active_membership) or new_uporabnina_valid_to > last_active_membership.valid_to:
                    add_membership = True
                else:
                    add_membership = False

                # add new membership to payment if user has no active membership or if new uporabnina is longer than current membership
                if (not (membership and membership.type and membership.type.plan and membership.active)) or add_membership:
                    paid_membership = MembershipType.objects.filter(plan__isnull=False).first()
                    plan = paid_membership.plan
                    price = plan.discounted_price if payment.user_was_eligible_to_discount else plan.price
                    payment.amount += price
                    payment.save()
                    PaymentPlan(plan=plan, payment=payment, price=price).save()

            promo_code_form = PromoCodeForm({'payment_id': payment.id})

            return render(request,'registration_payment_preview.html', { "payment": payment, "promo_code_form": promo_code_form, "purchase_type": purchase_type })
        else:
            return render(request, 'payment.html', { "id": None })

    def post(self, request):
        user = request.user

        promo_code_form = PromoCodeForm(request.POST)
        promo_code_error = False
        promo_code_success = False

        if promo_code_form.is_valid():
            registration = promo_code_form.cleaned_data["registration"]
            payment = Payment.objects.get(id=promo_code_form.cleaned_data["payment_id"])
            related_payment_plans = PaymentPlan.objects.filter(payment=payment)
            # check for promo code
            promo_code = promo_code_form.cleaned_data["promo_code"]
            if promo_code:
                promo_code_error = True
                for payment_plan in related_payment_plans:
                    if PromoCode.check_code_validity(promo_code, payment_plan):
                        valid_promo_code = PromoCode.objects.get(code=promo_code)
                        payment_plan.promo_code = valid_promo_code
                        payment_plan.save()
                        plan = payment_plan.plan
                        plan_price = plan.discounted_price if user.is_eligible_to_discount() else plan.price
                        payment.amount -= plan_price * Decimal(valid_promo_code.percent_discount / 100)
                        payment.save()
                        promo_code_error = False
                        promo_code_success = True

                        break

            return render(request,'registration_payment_preview.html', {
                "payment": payment,
                "promo_code_form": promo_code_form,
                "promo_code_error": promo_code_error,
                "promo_code_success": promo_code_success,
                "registration": registration
            })

        else:
            return render(request, 'payment.html', { "id": None })


@method_decorator(login_required, name='dispatch')
class Pay(views.APIView):
    def get(self, request):
        payment_id = request.GET.get('id', False)
        payment = get_object_or_404(Payment, id=payment_id)
        free_order = False
        if payment.amount == 0:
            # User has 100% discount dont show payment page
            finish_payment(payment)
            free_order = True
            payment.status = Payment.Status.SUCCESS
            payment.info = 'Plačano s promo kodo 100% popust'
            payment.successed_at = timezone.now()
            payment.invoice_number = get_invoice_number()
            payment.save()
        return render(request, 'payment.html', { "id": payment_id , "free_order": free_order})

    def post(self, request):
        print('INIT PAY')
        data = request.data
        payment_id = data.get('id', None)
        purchase_type = data.get('purchase_type', 'error')
        print("pay post purchase type", purchase_type)
        payment = get_object_or_404(Payment, id=payment_id)

        ids = settings.PAYMENT_IDS
        payment_url = settings.PAYMENT_BASE_URL
        id = payment.id
        # is_wizard = request.GET.get("wizard", False)
        redirect_url = f'{payment_url}?ids={ids}&id={id}&urlpar={purchase_type}'
        print("url za redirectat", redirect_url)

        response_data = {'redirect_url': redirect_url}
        return Response(response_data)


class PaymentDataXML(views.APIView):
    def get(self, request):
        payment_id = request.GET.get('id', None)
        payment = get_object_or_404(Payment, id=payment_id)
        user = payment.user
        opis_placila = 'Članarina'
        sifra_artikla = 1
        kolicina = 1
        # TODO fill in user data
        user_tax_id = ''
        user_name = ''
        user_address = ''
        user_city = ''
        user_post = ''
        user_email = user.email

        order_body = f'''
            <?xml version="1.0" encoding="UTF-8"?>
            <narocilo id="{payment_id}" maticna="{settings.REGISTRATION_NUMBER}" isoValuta="EUR" racun="{payment_id}" tipRacuna="1" xmlns="http://www.src.si/e-placila/narocilo/1.0">
                <opisPlacila>{opis_placila}</opisPlacila>
            <postavka sifraArtikla="{sifra_artikla}" imaProvizijo="false" konto="" podracun="" sklicPostavke="11">
                <opis>{opis_placila}</opis>
                <kolicina>{kolicina}</kolicina>
                <cena>{payment.amount}</cena>
            </postavka>
                <kupec sifraKupca="{user.id}">
                    <idZaDdv>{user_tax_id}</idZaDdv>
                    <naziv>{user_name}</naziv>
                    <naslov>{user_address}</naslov>
                    <kraj>{user_city}</kraj>
                    <posta>{user_post}</posta>
                    <eposta>{user_email}</eposta>
                    <poslano>false</poslano>
                </kupec>
                <referenca/>
            </narocilo>
        '''
        return HttpResponse(order_body.strip(), content_type='text/xml')


class PaymentSuccessXML(views.APIView):
    parser_classes = [XMLParser]
    def post(self, request):
        data = request.data
        print(data)

        payment_id = request.GET.get('id')
        payment = get_object_or_404(Payment, id=payment_id)

        if payment.successed_at:
            return Response({'status': 'Payment is already processed'})

        payment.status = Payment.Status.SUCCESS
        payment.info = str(data)
        payment.successed_at = timezone.now()
        payment.invoice_number = get_invoice_number()
        payment.save()

        finish_payment(payment)

        return Response({'status': 'OK'})


class PaymentSuccess(views.APIView):
    def get(self, request):

        if "registration" in request.GET:
            purchase_type = "registration"
        elif "plan" in request.GET:
            purchase_type = "plan"
        else:
            purchase_type = "membership"
        
        context_vars = {
            "purchase_type": purchase_type
        }

        if purchase_type == "registration":
            context_vars["registration_step"] = 5
        
        return render(request,'payment_success.html', context_vars)


class PaymentFailure(views.APIView):
    def get(self, request):
        data = request.data
        payment_id = data.get('id', None)
        payment = get_object_or_404(Payment, id=payment_id)
        payment.status = Payment.Status.ERROR
        payment.finished_at = timezone.now()
        payment.save()
        return render(request, 'payment_failed.html', {})


@method_decorator(login_required, name='dispatch')
class PaymentHistory(View):
    def get(self, request):
        user = request.user
        payments = user.payments.filter(successed_at__isnull=False).order_by('-created_at')

        return render(
            request,
            'payment_history.html',
            {
                'username': user.email.split('@')[0],
                'payments': payments
            }
        )


@method_decorator(login_required, name='dispatch')
class PaymentInvoice(View):
    def get(self, request, payment_id):
        user = request.user
        payment = user.payments.filter(id=payment_id).first()
        if payment:
            return render(
                request,
                'payment_invoice.html',
                {
                    'payment': payment,
                    'user': payment.user
                }
            )
        else:
            return HttpResponseNotFound('Računa ni mogoče najti.')


@method_decorator(login_required, name='dispatch')
class PaymentInvoicePDF(View):
    def get(self, request, payment_id):
        user = request.user
        payment = user.payments.filter(id=payment_id).first()
        if payment:
            return PDFTemplateResponse(
                request,
                'payment_invoice.html',
                {
                    'payment': payment,
                    'user': payment.user,
                },
                filename=f'rog-racun-{payment.id}.pdf',
                show_content_in_browser=True,
            )
        else:
            return HttpResponseNotFound('Računa ni mogoče najti.')
