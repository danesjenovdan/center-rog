from .models import Payment
from datetime import datetime


def get_invoice_number():
    year = datetime.now().strftime("%y")
    invoice_order = Payment.objects.filter(
        successed_at__year=datetime.now().year
    ).count() + 1
    invoice_order_str = str(invoice_order).zfill(3)
    return f'{year}-369-{invoice_order_str}'
