# Generated by Django 4.1.10 on 2023-08-09 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_alter_plan_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="pantheon_ident_id",
            field=models.CharField(default="test", max_length=100),
            preserve_default=False,
        ),
    ]
