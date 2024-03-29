# Generated by Django 4.1.10 on 2023-08-31 10:04

from django.db import migrations

def migrate_plans(apps, schema_editor):
    Payment = apps.get_model("payments", "Payment")
    PaymentPlan = apps.get_model("payments", "PaymentPlan")

    payments = Payment.objects.all()
    for payment in payments:
        if payment.plan:
            plan = payment.plan
            PaymentPlan(plan=plan, payment=payment, price=plan.price).save()


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_payment_items'),
    ]

    operations = [
        migrations.RunPython(migrate_plans)
    ]
