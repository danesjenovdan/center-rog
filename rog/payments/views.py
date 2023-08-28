from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework import  views
from rest_framework.response import Response
from datetime import timedelta

from .models import Payment, Plan, Token
from .parsers import XMLParser
from .pantheon import create_move
from home.email_utils import send_email


# Create your views here.

# payments
@method_decorator(login_required, name='dispatch')
class Pay(views.APIView):
    def get(self, request):
        plan_id = request.GET.get('plan_id', False)
        return render(request, 'payment.html', { "plan_id": plan_id })

    def post(self, request):
        print('INIT PAY')
        data = request.data
        payment = Payment(
            user=request.user,
        )
        if 'plan' in data.keys():
            plan = Plan.objects.get(id=data['plan'])
            payment.plan = plan
            payment.amount = plan.price
        payment.save()

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
        # set active_to if plan is subscription
        if payment.plan and payment.plan.is_subscription:
            payment.active_to = timezone.now() + timedelta(days=payment.plan.duration)
        payment.save()
        # create tokens
        Token.objects.bulk_create([
            Token(
                payment=payment,
                valid_from=timezone.now(),
                valid_to=timezone.now() + timedelta(days=payment.plan.duration)
            ) for i in range(payment.plan.tokens)
        ] + [
            Token(
                payment=payment,
                valid_from=timezone.now(),
                valid_to=timezone.now() + timedelta(days=payment.plan.duration),
                type_of=Token.Type.WORKSHOP
            ) for i in range(payment.plan.workshops)
        ])
        items = [
            {
                'quantity': 1,
                'name': payment.plan.name,
                'price': payment.amount,
            }
        ]
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
