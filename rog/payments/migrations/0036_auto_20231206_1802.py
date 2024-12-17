# Generated by Django 4.1.11 on 2023-12-06 17:02

from django.db import migrations


def migrate_payment_item_type(apps, schema_editor):
    Plan = apps.get_model("payments", "Plan")
    PromoCode = apps.get_model("payments", "PromoCode")

    plans = Plan.objects.all()
    for plan in plans:
        plan.payment_item_type = plan.item_type.name
        plan.save()

    promo_codes = PromoCode.objects.all()
    for promo_code in promo_codes:
        promo_code.payment_item_type = promo_code.item_type.name
        promo_code.save()


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0035_remove_paymentplanevent_event_and_more"),
    ]

    operations = [migrations.RunPython(migrate_payment_item_type)]
