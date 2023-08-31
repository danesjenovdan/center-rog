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

from .models import Payment, Plan, Token, PaymentPlan
from users.models import Membership, MembershipType
from .parsers import XMLParser
from .pantheon import create_move
from home.email_utils import send_email


# Create your views here.

# payments
class PaymentPreview(views.APIView):
    def get(self, request):
        plan_id = request.GET.get('plan_id', False)
        user = request.user
        payment = Payment(
            user=user,
        )

        plan = Plan.objects.get(id=plan_id)
        payment.user_was_eligible_to_discount = user.is_eligible_to_discount()
        price = plan.discounted_price if payment.user_was_eligible_to_discount else plan.price
        payment.amount = price
        payment.save()
        PaymentPlan(plan=plan, payment=payment, price=price).save()

        membership = user.membership
        if not (membership and membership.type and membership.type.plan):
            paid_membership = MembershipType.objects.filter(plan__isnull=False).first()
            plan = paid_membership.plan
            payment.amount += plan.price
            payment.save()
            PaymentPlan(plan=plan, payment=payment, price=plan.price).save()

        return render(request,'registration_payment_preview.html', { "registration_step": 5, "payment": payment })


@method_decorator(login_required, name='dispatch')
class Pay(views.APIView):
    def get(self, request):
        payment_id = request.GET.get('id', False)
        return render(request, 'payment.html', { "id": payment_id })

    def post(self, request):
        print('INIT PAY')
        data = request.data
        payment = get_object_or_404(Payment, id=data['id'])

        ids = settings.PAYMENT_IDS
        payment_url = settings.PAYMENT_BASE_URL
        id = payment.id
        is_wizard = request.GET.get("wizard", False)
        redirect_url = f'{payment_url}?ids={ids}&id={id}&{"urlpar=wizard" if is_wizard else ""}'
        response_data = {'redirect_url': redirect_url}
        return Response(response_data)


class PaymentDataXML(views.APIView):
    def get(self, request):
        payment_id = request.GET.get('id')
        payment = Payment.objects.get(id=payment_id)
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
        payment = Payment.objects.get(id=payment_id)
        payment.status = Payment.Status.SUCCESS
        payment.info = str(data)
        payment.successed_at = timezone.now()

        # membership
        membership_fee = payment.items.filter(item_type__name__icontains='clanarina')
        if membership_fee:
            membership = request.user.membership
            if not membership:
                membership_type = MembershipType.objects.filter(plan=membership_fee).first()
                today = datetime.now()
                one_year_from_now = today + relativedelta(years=1)
                Membership(valid_from=today, valid_to=one_year_from_now, type=membership_type, active=True, user=request.user).save()
            else:
                membership.active = True
                membership.save()

        # set active_to if plan is subscription
        items = []
        for plan in payment.items.all():
            if plan and plan.is_subscription:
                payment.active_to = timezone.now() + timedelta(days=plan.duration)
            payment.save()
            # create tokens
            if plan.item_type and plan.item_type.name == 'Uporabnina':
                Token.objects.bulk_create([
                    Token(
                        payment=payment,
                        valid_from=timezone.now(),
                        valid_to=timezone.now() + timedelta(days=plan.duration)
                    ) for i in range(plan.tokens)
                ] + [
                    Token(
                        payment=payment,
                        valid_from=timezone.now(),
                        valid_to=timezone.now() + timedelta(days=plan.duration),
                        type_of=Token.Type.WORKSHOP
                    ) for i in range(plan.workshops)
                ])
            items.append({
                'quantity': 1,
                'name': plan.name,
                'price': plan.price,
            })

        send_email(
            payment.user.email,
            'emails/order.html',
            _('Naročilo rog'),
            {
                'items': items,
                'date': payment.successed_at
            }
        )


        return Response({'status': 'OK'})


class PaymentSuccess(views.APIView):
    def get(self, request):
        if "wizard" in request.GET:
            return render(request,'registration_payment_success.html', { "registration_step": 5 })
        else:
            return render(request, 'payment_success.html', {})


class PaymentFailure(views.APIView):
    def get(self, request):
        data = request.data
        payment = Payment.objects.get(id=data['id'])
        payment.status = Payment.Status.ERROR
        payment.finished_at = timezone.now()
        payment.save()
        return render(request, 'payment_failed.html', {})


@method_decorator(login_required, name='dispatch')
class PaymentHistory(View):
    def get(self, request):
        user = request.user
        payments = user.payments.all().order_by('-created_at')

        return render(
            request,
            'payment_hystory.html',
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
