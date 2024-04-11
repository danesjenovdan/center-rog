from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.utils import timezone
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework import views
from rest_framework.response import Response
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from wkhtmltopdf.views import PDFTemplateResponse
from decimal import Decimal
from sentry_sdk import capture_message

from .models import Payment, Plan, PaymentPlanEvent, PromoCode, PaymentItemType
from users.models import Membership, MembershipType
from .parsers import XMLParser
from .forms import PromoCodeForm
from .utils import get_invoice_number, get_free_invoice_number, finish_payment
from events.models import EventRegistration

# Create your views here.


@method_decorator(login_required, name="dispatch")
class PaymentPreview(views.APIView):
    def get(self, request):
        plan_id = request.GET.get("plan_id", False)
        purchase_type = request.GET.get("purchase_type", "")
        membership_id = request.GET.get("membership", False)
        event_registration_id = request.GET.get("event_registration", False)
        user = request.user

        if plan_id:
            plan = Plan.objects.filter(id=plan_id).first()

            if plan and user:
                payment = Payment(
                    user=user,
                )
                payment.user_was_eligible_to_discount = user.is_eligible_to_discount()
                price = (
                    plan.discounted_price
                    if payment.user_was_eligible_to_discount
                    else plan.price
                )
                payment.amount = price
                payment.original_amount = plan.price
                if membership_id:
                    membership = Membership.objects.get(id=membership_id)
                    payment.membership = membership
                payment.save()
                PaymentPlanEvent(
                    plan=plan,
                    payment=payment,
                    price=price,
                    plan_name=plan.name,
                    original_price=plan.price,
                    payment_item_type=plan.payment_item_type,
                ).save()

                if plan.payment_item_type == PaymentItemType.UPORABNINA:
                    # if plan is uporabnina add clanarina to payment
                    membership = user.membership

                    # check if user has active membership for entire duration of new uporabnina
                    last_payment_plan = (
                        user.payments.get_last_active_subscription_payment_plan()
                    )
                    valid_to = (
                        last_payment_plan.valid_to
                        if last_payment_plan and last_payment_plan.valid_to
                        else timezone.now()
                    )
                    new_uporabnina_valid_to = valid_to + timedelta(days=plan.duration)
                    last_active_membership = user.get_last_active_membership()

                    # add new membership to payment if user has no active membership or if new uporabnina is longer than current membership
                    if (
                        not last_active_membership
                    ) or ((new_uporabnina_valid_to > last_active_membership.valid_to) and not plan.extend_membership):
                        today = datetime.now()
                        one_year_from_now = today + timedelta(days=365)
                        paid_membership_type = MembershipType.objects.filter(
                            plan__isnull=False
                        ).first()
                        membership = Membership(
                            valid_from=today,
                            valid_to=one_year_from_now,
                            type=paid_membership_type,
                            active=False,
                            user=user,
                        )
                        membership.save()

                        plan = paid_membership_type.plan
                        price = (
                            plan.discounted_price
                            if payment.user_was_eligible_to_discount
                            else plan.price
                        )
                        payment.amount += price
                        payment.original_amount += plan.price
                        payment.membership = membership
                        payment.save()
                        PaymentPlanEvent(
                            plan=plan,
                            payment=payment,
                            price=price,
                            original_price=plan.price,
                            plan_name=plan.name,
                            payment_item_type=plan.payment_item_type,
                        ).save()

                promo_code_form = PromoCodeForm({"payment_id": payment.id})

                return render(
                    request,
                    "registration_payment_preview.html",
                    {
                        "payment": payment,
                        "promo_code_form": promo_code_form,
                        "purchase_type": purchase_type,
                    },
                )
            else:
                return redirect("profile-my")
        elif event_registration_id:
            event_registration = get_object_or_404(
                EventRegistration, id=event_registration_id
            )
            event = event_registration.event
            if event_registration.user != user:
                # user is not owner of event registration
                return redirect("profile-my")

            if event_registration and user:
                people_count = event_registration.event_registration_children.count()
                title = event.title
                if people_count == 0:
                    people_count = 1
                else:
                    title = f"{title} x {people_count}"

                # check if there is enough free places
                free_places = event.get_free_places()
                if people_count > free_places:
                    return render(
                        request,
                        "events/event_registration_failed.html",
                        context={"registration_step": 4},
                    )

                if user.membership:
                    price = event.price * people_count
                else:
                    price = event.price_for_non_member * people_count

                existing_payment_plan = event_registration.payment_plans.first()
                if existing_payment_plan:
                    payment = existing_payment_plan.payment
                    existing_payment_plan.price = price
                    existing_payment_plan.original_price = price
                    existing_payment_plan.plan_name=title
                    existing_payment_plan.save()
                    payment.amount = price
                    payment.original_amount = price
                    payment.save()
                else:
                    payment = Payment(
                        user=user,
                    )
                    payment.amount = price
                    payment.original_amount = price
                    payment.save()
                    PaymentPlanEvent(
                        payment_item_type=(
                            PaymentItemType.TRAINING
                            if event.category and (event.category.name == "Usposabljanja")
                            else PaymentItemType.EVENT
                        ),
                        event_registration=event_registration,
                        payment=payment,
                        original_price=price,
                        price=price,
                        plan_name=title,
                    ).save()

                promo_code_form = PromoCodeForm({"payment_id": payment.id})

                return render(
                    request,
                    "registration_payment_preview.html",
                    {
                        "payment": payment,
                        "promo_code_form": promo_code_form,
                        "purchase_type": purchase_type,
                    },
                )
            else:
                return redirect("profile-my")
        else:
            return redirect("profile-my")

    def post(self, request):
        user = request.user

        purchase_type = request.GET.get("purchase_type", "")

        promo_code_form = PromoCodeForm(request.POST)
        promo_code_error = False
        promo_code_success = False

        if promo_code_form.is_valid():
            registration = promo_code_form.cleaned_data["registration"]
            payment = Payment.objects.get(id=promo_code_form.cleaned_data["payment_id"])
            related_payment_plans = PaymentPlanEvent.objects.filter(payment=payment)
            # check for promo code
            promo_code = promo_code_form.cleaned_data["promo_code"]
            if promo_code:
                promo_code_error = True
                for payment_plan in related_payment_plans:
                    if payment_plan.promo_code:
                        continue
                    if PromoCode.check_code_validity(promo_code, payment_plan):
                        if payment_plan.payment_item_type in [PaymentItemType.EVENT, PaymentItemType.TRAINING]:
                            valid_promo_code = PromoCode.objects.get(code=promo_code)
                            payment_plan.promo_code = valid_promo_code
                            payment_plan.save()
                            payment.amount -= payment_plan.price * Decimal(
                                valid_promo_code.percent_discount / 100
                            )
                            payment.save()
                            payment_plan.price = payment_plan.price - payment_plan.price * Decimal(
                                valid_promo_code.percent_discount / 100
                            )
                            payment_plan.save()
                            promo_code_error = False
                            promo_code_success = True

                            break
                        else:
                            valid_promo_code = PromoCode.objects.get(code=promo_code)
                            payment_plan.promo_code = valid_promo_code
                            payment_plan.save()
                            plan = payment_plan.plan
                            plan_price = (
                                plan.discounted_price
                                if user.is_eligible_to_discount()
                                else plan.price
                            )
                            payment.amount -= plan_price * Decimal(
                                valid_promo_code.percent_discount / 100
                            )
                            payment.save()
                            payment_plan.price = plan_price - plan_price * Decimal(
                                valid_promo_code.percent_discount / 100
                            )
                            payment_plan.save()
                            promo_code_error = False
                            promo_code_success = True

                            break

            return render(
                request,
                "registration_payment_preview.html",
                {
                    "payment": payment,
                    "promo_code_form": promo_code_form,
                    "promo_code_error": promo_code_error,
                    "promo_code_success": promo_code_success,
                    "registration": registration,
                    "purchase_type": purchase_type,
                },
            )

        else:
            return render(request, "payment.html", {"id": None})


@method_decorator(login_required, name="dispatch")
class Pay(views.APIView):
    def get(self, request):
        payment_id = request.GET.get("id", 0)
        payment = get_object_or_404(Payment, id=payment_id)
        if payment.user != request.user:
            # user is not owner of event registration
            return redirect("profile-my")
        free_order = False
        if payment.amount == 0:
            # User has 100% discount dont show payment page
            last_ujp_payment = Payment.objects.all().exclude(ujp_id=None).order_by('-ujp_id')[0]
            payment.ujp_id = last_ujp_payment.ujp_id + 1
            finish_payment(payment)
            free_order = True
            payment.status = Payment.Status.SUCCESS.value
            payment.info = "Plačano s promo kodo 100% popust"
            payment.successed_at = timezone.now()
            payment.invoice_number = get_free_invoice_number()
            payment.save()
        return render(
            request, "payment.html", {"id": payment_id, "ujp_id": payment.ujp_id, "free_order": free_order}
        )

    def post(self, request):
        data = request.data
        payment_id = data.get("id", 0)
        purchase_type = data.get("purchase_type", "error")
        payment = get_object_or_404(Payment, id=payment_id)

        if payment.user != request.user:
            # user is not owner of event registration
            return redirect("profile-my")

        if payment.status == Payment.Status.SUCCESS:
            return render(request, "payment_failed.html", {"status": _("Plačilo je bilo že sprocesirano.")})

        uuid = payment.user.uuid

        # increase ujp id
        last_ujp_payment = Payment.objects.all().exclude(ujp_id=None).order_by('-ujp_id')[0]
        payment.ujp_id = last_ujp_payment.ujp_id + 1
        payment.save()

        id = payment.ujp_id
        redirect_url = f"{settings.PAYMENT_BASE_URL}vstop/index?ids={settings.PAYMENT_IDS}&id={id}&urlpar=args={purchase_type},{uuid}"

        response_data = {"redirect_url": redirect_url}
        return Response(response_data)


class PaymentDataXML(views.APIView):
    def get(self, request):
        print(request.META)
        payment_ujp_id = request.GET.get("id", 0)
        urlpar = request.GET.get("args", "")
        urlpars = urlpar.split(",")

        if len(urlpars) < 2:
            print(urlpars)
            return Response({"status": "Not enough urlpar values"}, status=400)

        payment = get_object_or_404(Payment, ujp_id=payment_ujp_id)

        if str(payment.user.uuid) != urlpars[1]:
            print("uuid does not match")
            return Response({"status": "UUID does not match"}, status=400)

        user = payment.user
        # TODO fill in user data
        user_tax_id = user.legal_person_tax_number
        user_name = f"{payment.user.first_name} {payment.user.last_name}"
        user_address = user.address_1
        user_city = ""
        user_post = user.get_post()
        user_email = user.email
        items = ""

        for pp in payment.payment_plans.all():
            if pp.payment_item_type in [PaymentItemType.EVENT, PaymentItemType.TRAINING]:
                sifra = payment.payment_plans.first().event_registration.event.id
            else:
                sifra = pp.plan.id
            items = (
                items
                + f"""
            <postavka sifraArtikla="{sifra}" imaProvizijo="false" konto="" podracun="" sklicPostavke="11">
                <opis>{pp.plan_name}</opis>
                <kolicina>1</kolicina>
                <cena>{pp.price}</cena>
            </postavka>
            """
            )

        year = payment.created_at.year

        reference = f"{year}-369-{payment.ujp_id}"
        sklic = f"SI00{year}369{payment.ujp_id}"
        opis_placila = f"Plačilo računa za {user_name}"

        order_body = f"""
            <?xml version="1.0" encoding="UTF-8"?>
            <narocilo id="{payment_ujp_id}" maticna="{settings.REGISTRATION_NUMBER}" isoValuta="EUR" racun="{payment_ujp_id}" tipRacuna="1" xmlns="http://www.src.si/e-placila/narocilo/1.0">
                <opisPlacila>{opis_placila}</opisPlacila>
                <referenca>{reference}</referenca>
                <sklicDobro>{sklic}</sklicDobro>
            {items}
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
        """
        return HttpResponse(order_body.strip(), content_type="text/xml")


class PaymentSuccessXML(views.APIView):
    parser_classes = [XMLParser]

    def post(self, request):
        data = request.data
        print(data)

        payment_ujp_id = request.GET.get("id", 0)
        urlpar = request.GET.get("args", "")
        urlpars = urlpar.split(",")

        if len(urlpars) < 2:
            print(urlpars)
            return Response({"status": "Not enough urlpar values"}, status=400)

        payment = get_object_or_404(Payment, ujp_id=payment_ujp_id)

        # check_url = f'{settings.PAYMENT_BASE_URL}cert/rezultat/potrdilo?ids={settings.PAYMENT_IDS}&id={payment.ujp_id}',
        # check_response = requests.get(check_url)

        # print('Success')
        # print(check_response.content)
        # print(check_response.status_code)

        if str(payment.user.uuid) != urlpars[1]:
            return Response({"status": "UUID does not match"}, status=400)

        if payment.successed_at:
            return Response({"status": "Payment is already processed"})

        payment.info = str(data)
        payment.save()
        if '<rezultat>1</rezultat>' in payment.info:
            if payment.status == Payment.Status.SUCCESS:
                capture_message(f"Payment {payment.id} is SUCCESSED and UJP result is 1. Investigete it!", 'fatal')
            else:
                payment.status = Payment.Status.ERROR.value
                payment.errored_at = timezone.now()
                payment.save()
        elif '<rezultat>0</rezultat>' in payment.info:
            payment.transaction_success_at = timezone.now()
            payment.refresh_from_db()
            if payment.status != Payment.Status.SUCCESS:
                """
                payment is marked as successed on redirect page from UJP,
                if user closes page before redirect payment is not marked as successed
                """
                payment.status = Payment.Status.SUCCESS.value
                payment.successed_at = timezone.now()
                payment.invoice_number = get_invoice_number()
                payment.save()
                finish_payment(payment)
            else:
                payment.save()

        return Response({"status": "OK"})


class PaymentSuccess(views.APIView):
    def get(self, request):
        context_vars = {}
        args = request.GET.get("args", "")
        urlpar = request.GET.get("args", "")
        urlpars = urlpar.split(",")
        free_order = request.GET.get("free_order", False)

        # free order has no args and different HTTP_REFERER

        if not free_order and len(urlpars) < 2:
            return render(request, "payment_failed.html", {"status": _("Napaka pri plačilu.")})

        payment = Payment.objects.get(ujp_id=request.GET.get('id'))

        if free_order:
            if payment.status != Payment.Status.SUCCESS:
                capture_message(f"Payment {payment.id} is not SUCCESSED and free_order is True. Investigete it!", 'fatal')
                return render(request, "payment_failed.html", {"status": _("Napaka pri plačilu.")})

        # check if referer exists and is valid
        referer = request.META.get('HTTP_REFERER')
        if not free_order and not (referer and referer.startswith(settings.PAYMENT_BASE_URL)):
            capture_message(f'Payment referer is not valid {settings.PAYMENT_BASE_URL} != {referer}. Payment id {payment.id} Investigate it!', 'fatal')
            return render(request, "payment_failed.html", {'status': 'Napaka pri plačilu'})

        print(args)
        if "registration" in args:
            purchase_type = "registration"
        elif "plan" in args:
            purchase_type = "plan"
        elif "event" in args:
            purchase_type = "event"
            event = payment.payment_plans.first().event_registration.event
            context_vars['event'] = event
        else:
            purchase_type = "membership"

        context_vars["purchase_type"] = purchase_type

        if purchase_type == "registration":
            context_vars["registration_step"] = 5

        if free_order:
            # Free order has already status.SUCCESS
            return render(request, "payment_success.html", context_vars)

        if str(payment.user.uuid) != urlpars[1]:
            return render(request, "payment_failed.html",{"status": "UUID does not match"})

        payment.refresh_from_db()
        if payment.status != Payment.Status.SUCCESS:
            payment.status = Payment.Status.SUCCESS.value
            payment.successed_at = timezone.now()
            payment.invoice_number = get_invoice_number()
            payment.save()
            finish_payment(payment)

        return render(request, "payment_success.html", context_vars)


class PaymentFailure(views.APIView):
    def get(self, request):
        payment_ujp_id = request.GET.get("id", 0)
        payment = get_object_or_404(Payment, ujp_id=payment_ujp_id)
        return render(request, "payment_failed.html", {})


@method_decorator(login_required, name="dispatch")
class PaymentHistory(View):
    def get(self, request):
        user = request.user
        payments = user.payments.filter(successed_at__isnull=False).order_by(
            "-created_at"
        )

        return render(
            request,
            "payment_history.html",
            {"username": user.email.split("@")[0], "payments": payments},
        )


@method_decorator(login_required, name="dispatch")
class PaymentInvoice(View):
    def get(self, request, payment_id):
        user = request.user
        payment = user.payments.filter(id=payment_id).first()
        if payment:
            return render(
                request,
                "payment_invoice.html",
                {"payment": payment, "user": payment.user},
            )
        else:
            return HttpResponseNotFound("Računa ni mogoče najti.")


@method_decorator(login_required, name="dispatch")
class PaymentInvoicePDF(View):
    def get(self, request, payment_id):
        user = request.user
        payment = user.payments.filter(id=payment_id).first()
        if payment:
            return PDFTemplateResponse(
                request,
                "payment_invoice.html",
                {
                    "payment": payment,
                    "user": payment.user,
                },
                filename=f"rog-racun-{payment.ujp_id}.pdf",
                show_content_in_browser=True,
            )
        else:
            return HttpResponseNotFound("Računa ni mogoče najti.")
