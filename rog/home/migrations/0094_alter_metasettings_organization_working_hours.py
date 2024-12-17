# Generated by Django 4.1.11 on 2023-09-21 11:22

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0093_alter_contentpage_body_alter_contentpage_body_en_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="metasettings",
            name="organization_working_hours",
            field=wagtail.fields.StreamField(
                [
                    (
                        "time",
                        wagtail.blocks.StructBlock(
                            [
                                ("day", wagtail.blocks.CharBlock(label="Dan")),
                                (
                                    "start_time",
                                    wagtail.blocks.TimeBlock(label="Začetna ura"),
                                ),
                                (
                                    "end_time",
                                    wagtail.blocks.TimeBlock(label="Končna ura"),
                                ),
                            ],
                            label="Dan in ura",
                        ),
                    ),
                    (
                        "notice",
                        wagtail.blocks.StructBlock(
                            [
                                ("day", wagtail.blocks.CharBlock(label="Dan")),
                                ("text", wagtail.blocks.CharBlock(label="Opomba")),
                            ],
                            label="Dan in opomba",
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=True,
                verbose_name="Delovni čas organizacije",
            ),
        ),
    ]
