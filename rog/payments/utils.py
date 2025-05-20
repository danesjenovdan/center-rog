from django.utils import timezone

from .models import Payment, PromoCode, Token, PaymentPlanEvent, PaymentItemType
from users.models import Membership, MembershipType
from home.email_utils import send_email

from datetime import datetime, timedelta

from sentry_sdk import capture_message, push_scope

from users.prima_api import PrimaApi

prima_api = PrimaApi()


def get_invoice_number():
    year = datetime.now().strftime("%y")
    invoice_order = Payment.objects.filter(
        transaction_success_at__year=datetime.now().year,
        amount__gt=0
    ).count() + 1  + 28 # WORKAROUND shift invoice number 
    invoice_order_str = str(invoice_order).zfill(6)
    return f'{year}-369-{invoice_order_str}'

def get_free_invoice_number():
    year = datetime.now().strftime("%y")
    invoice_order = Payment.objects.filter(
        successed_at__year=datetime.now().year,
        amount=0
    ).count() + 1
    invoice_order_str = str(invoice_order).zfill(6)
    return f'{year}-000-{invoice_order_str}'

def finish_payment(payment):
    user_fee_plan = None
    event = None
    first_membership_paid = False
    user = payment.user
    membership_fee = payment.items.filter(payment_item_type=PaymentItemType.CLANARINA)
    membership = payment.membership
    if membership_fee and membership:
        valid_from = timezone.now()

        last_active_membership = user.get_last_active_membership()

        # check if it's first payable membership
        if not last_active_membership:
            first_membership_paid = True

        if last_active_membership:
            # user has active membership
            valid_from = last_active_membership.valid_to
            if valid_from < timezone.now():
                valid_from = timezone.now()

        valid_to = valid_from + timedelta(days=365)
        membership.valid_from = valid_from
        membership.valid_to = valid_to
        membership.active = True
        membership.save()

        if not user.prima_id:
            # create PRIMA user
            data, message = prima_api.createUser(user.email)
            print(data)
            if data:
                prima_id = data["UsrID"]
                user.prima_id = prima_id
                user.save()
                # set prima uporabnina valid dates to now
                valid_from_prima = timezone.now()
                valid_to_prima = valid_from_prima
                valid_from_prima_string = valid_from_prima.strftime('%Y-%m-%d %H:%M:%S')
                valid_to_prima_string = valid_to_prima.strftime('%Y-%m-%d %H:%M:%S')
                prima_api.setUporabninaDates(prima_id, valid_from_prima_string, valid_to_prima_string)
            else:
                msg = f"Prima user was not created successfully: {message}"
                with push_scope() as scope:
                    scope.user = {"user": user}
                    scope.set_extra("membership", membership.id)
                    scope.set_extra("payment", payment.id)
                    capture_message(msg, "fatal")

    elif membership_fee or membership:
        # send error to sentry
        msg = f"Integrity error: payment.membership or payment.items.clanarina_fee is missing"
        with push_scope() as scope:
            scope.user = { "user" : user}
            scope.set_extra("membership", membership.id)
            scope.set_extra("payment", payment.id)
            capture_message(msg, 'fatal')

    # set valid_to if plan is subscription
    items = []
    for payment_plan in payment.payment_plans.all():
        plan = payment_plan.plan
        # create tokens
        if payment_plan.payment_item_type == PaymentItemType.UPORABNINA:
            user_fee_plan = plan
            last_payment_plan = user.payments.get_last_active_subscription_payment_plan()
            valid_from = last_payment_plan.valid_to if last_payment_plan and last_payment_plan.valid_to else timezone.now()
            valid_to = valid_from + timedelta(days=plan.duration)

            # extend membership if plan is expandable and user does not have enough membership
            if plan.extend_membership:
                last_active_membership = user.get_last_active_membership()
                if last_active_membership.valid_to < valid_to:
                    membership = Membership(
                        valid_from=last_active_membership.valid_to,
                        valid_to=valid_to,
                        type=last_active_membership.type,
                        active=True,
                        user=user,
                        extended_by=plan
                    )
                    membership.save()

            Token.objects.bulk_create([
                Token(
                    payment=payment,
                    valid_from=valid_from,
                    valid_to=valid_from + timedelta(days=plan.duration)
                ) for i in range(plan.tokens)
            ] + [
                Token(
                    payment=payment,
                    valid_from=valid_from,
                    valid_to=valid_from + timedelta(days=plan.duration),
                    type_of=Token.Type.WORKSHOP
                ) for i in range(plan.workshops)
            ])

        if payment_plan.payment_item_type in [PaymentItemType.EVENT, PaymentItemType.TRAINING]:
            event_registration = payment_plan.event_registration
            event_registration.registration_finished = True
            event_registration.save()
            event = event_registration.event

        items.append({
            'quantity': 1,
            'name': payment_plan.plan_name,
            'price': payment_plan.price,
        })

    payment_plans = PaymentPlanEvent.objects.filter(payment=payment)
    for payment_plan in payment_plans:
        if payment_plan.promo_code:
            payment_plan.promo_code.use_code()

    payment.payment_done_at = timezone.now()
    payment.save()

    if first_membership_paid:
        send_email(
            payment.user.email,
            "emails/first_membership_paid.html",
            f"Center Rog – uspešen zakup članstva // successful membership purchase",
            {
                "membership": membership,
                "name": payment.user.first_name,
            },
        )

    if user_fee_plan:
        send_email(
            payment.user.email,
            "emails/order_user_fee.html",
            f"Center Rog – uspešen zakup paketa { user_fee_plan.name } za odprte termine v labih Centra Rog // successful purchase of user package { user_fee_plan.name } for individual work at Center Rog labs",
            {"plan": user_fee_plan, "name": payment.user.first_name},
        )

    if event:
        send_email(
            payment.user.email,
            "emails/order_event.html",
            f"Center Rog – uspešna prijava na dogodek // successful sign-up to the event",
            {"event": event, "name": payment.user.first_name},
        )
