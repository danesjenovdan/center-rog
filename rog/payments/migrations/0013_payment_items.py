# Generated by Django 4.1.10 on 2023-08-31 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0012_payment_user_was_eligible_to_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="items",
            field=models.ManyToManyField(
                help_text="Items in payment",
                related_name="payments",
                to="payments.plan",
            ),
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, blank=True, null=True
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="payments.payment",
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="payments.plan"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="payment",
            name="items",
            field=models.ManyToManyField(
                help_text="Items in payment",
                related_name="payments",
                through="payments.PaymentPlan",
                to="payments.plan",
            ),
        ),
    ]
