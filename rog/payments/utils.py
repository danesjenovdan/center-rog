from django.utils import timezone

from .models import Payment, Token, PaymentPlanEvent, PaymentItemType
from users.models import Membership, MembershipType
from home.email_utils import send_email

from datetime import datetime, timedelta

from sentry_sdk import capture_message, push_scope

from users.prima_api import PrimaApi

prima_api = PrimaApi()


def get_invoice_number():
    year = datetime.now().strftime("%y")
    invoice_order = Payment.objects.filter(
        successed_at__year=datetime.now().year
    ).count() + 1
    invoice_order_str = str(invoice_order).zfill(3)
    return f'{year}-369-{invoice_order_str}'


def finish_payment(payment):
    user_fee_plan = None
    event = None
    user = payment.user
    membership_fee = payment.items.filter(payment_item_type=PaymentItemType.CLANARINA)
    membership = payment.membership
    if membership_fee and membership:
        valid_from = timezone.now()

        last_active_membership = user.get_last_active_membership()
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

        valid_from_prima = valid_from.strftime('%Y-%m-%d %H:%M:%S')
        valid_to_prima = valid_to.strftime('%Y-%m-%d %H:%M:%S')
        prima_api.setUporabninaDates(user.prima_id, valid_from_prima, valid_to_prima)
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
            payment_plan.valid_to = valid_from + timedelta(days=plan.duration)
            payment_plan.save()

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

        if payment_plan.payment_item_type == PaymentItemType.EVENT:
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

    if user_fee_plan:
        send_email(
            payment.user.email,
            'emails/order_user_fee.html',
            f'Center Rog – uspešen zakup paketa {user_fee_plan.name} za odprte termine',
            {
                'plan': user_fee_plan
            }
        )

    if event:
        send_email(
            payment.user.email,
            'emails/order_event.html',
            f'Center Rog – uspešna prijava na dogodek',
            {
                'event': event
            }
        )
