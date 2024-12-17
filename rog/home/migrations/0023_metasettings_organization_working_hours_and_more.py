# Generated by Django 4.1.9 on 2023-06-21 06:21

import wagtail.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0022_metasettings_social_media_facebook_and_more"),
    ]

    operations = [
        migrations.AddField(
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
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="labpage",
            name="working_hours",
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
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="librarypage",
            name="working_hours",
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
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="marketstorepage",
            name="working_hours",
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
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="residencepage",
            name="working_hours",
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
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="studiopage",
            name="working_hours",
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
                    )
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
