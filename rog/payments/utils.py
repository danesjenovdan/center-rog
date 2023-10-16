from django.utils import timezone

from .models import Payment, Token, PaymentPlan
from users.models import Membership, MembershipType
from home.email_utils import send_email

from datetime import datetime, timedelta



def get_invoice_number():
    year = datetime.now().strftime("%y")
    invoice_order = Payment.objects.filter(
        successed_at__year=datetime.now().year
    ).count() + 1
    invoice_order_str = str(invoice_order).zfill(3)
    return f'{year}-369-{invoice_order_str}'


def finish_payment(payment):
    # membership
    user = payment.user
    membership_fee = payment.items.filter(item_type__name__icontains='clanarina')
    if membership_fee:
        membership = user.membership
        membership_type = MembershipType.objects.filter(plan=membership_fee.first()).first()

        if not membership:
            # User has no membership at this time
            valid_from = timezone.now()

            valid_to = valid_from + timedelta(days=365)
            Membership(
                valid_from=valid_from,
                valid_to=valid_to,
                type=membership_type,
                active=True,
                user=user
            ).save()
        else:
            last_active_membership = user.get_last_active_membership()
            if last_active_membership:
                # user has active membership
                valid_from = last_active_membership.valid_to
                if valid_from < timezone.now():
                    valid_from = timezone.now()
                valid_to = valid_from + timedelta(days=365)
                Membership(
                    valid_from=valid_from,
                    valid_to=valid_to,
                    type=membership_type,
                    active=True,
                    user=user
                ).save()
            else:
                # user has free membership
                membership.active = True
                membership.valid_from = valid_from
                membership.valid_to = valid_from + timedelta(days=365)
                membership.save()

    user_fee_plan = None # uporabnina

    # set valid_to if plan is subscription
    items = []
    for payment_plan in payment.payment_plans.all():
        plan = payment_plan.plan
        # create tokens
        if plan.item_type and plan.item_type.name == 'uporabnina':
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
        items.append({
            'quantity': 1,
            'name': plan.name,
            'price': plan.price,
        })

    payment_plans = PaymentPlan.objects.filter(payment=payment)
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
