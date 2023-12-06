# Generated by Django 4.1.11 on 2023-12-05 15:04

from django.db import migrations

def migrate_original_price(apps, schema_editor):
    PaymentPlan = apps.get_model("payments", "PaymentPlan")

    payment_plans = PaymentPlan.objects.all()
    for payment_plan in payment_plans:
        payment_plan.original_price = payment_plan.plan.price
        payment_plan.save()

class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0034_paymentplan_original_price'),
    ]

    operations = [
        migrations.RunPython(migrate_original_price)
    ]
