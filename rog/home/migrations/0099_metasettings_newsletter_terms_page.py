# Generated by Django 4.1.11 on 2023-10-09 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("home", "0098_alter_contentpage_body_alter_contentpage_body_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="metasettings",
            name="newsletter_terms_page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailcore.page",
            ),
        ),
    ]
