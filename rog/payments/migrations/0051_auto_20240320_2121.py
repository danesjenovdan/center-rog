# Generated by Django 4.1.11 on 2024-03-20 20:21

from django.db import migrations

def migrate_promocodes_types(apps, schema_editor):
    PromoCode = apps.get_model("payments", "PromoCode")

    codes = PromoCode.objects.filter(payment_item_type="event")
    codes.update(payment_item_type="training")


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0050_promocode_usage_limit'),
    ]

    operations = [
        migrations.RunPython(migrate_promocodes_types)
    ]