# Generated by Django 4.1.11 on 2024-04-15 11:47

import django.db.models.deletion
import wagtail.blocks
import wagtail.blocks.field_block
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("home", "0106_labpage_button_text_en_labpage_button_text_sl"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkingStationPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "color_scheme",
                    models.CharField(
                        choices=[
                            ("brown", "Rjava"),
                            ("light-gray", "Svetlo siva"),
                            ("dark-gray", "Temno siva"),
                            ("light-blue", "Svetlo modra"),
                            ("dark-blue", "Temno modra"),
                            ("light-green", "Svetlo zelena"),
                            ("dark-green", "Temno zelena"),
                            ("dark-purple", "Temno vijolična"),
                            ("light-purple", "Svetlo vijolična"),
                            ("red", "Rdeča"),
                            ("beige", "Bež"),
                            ("beige-gray", "Umazana siva"),
                            ("orange", "Oranžna"),
                            ("pink", "Roza"),
                            ("yellow", "Rumena"),
                            ("white", "Bela"),
                        ],
                        default="light-green",
                        max_length=20,
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Kratek opis na kartici"),
                ),
                (
                    "modules",
                    wagtail.fields.StreamField(
                        [
                            (
                                "bulletpoints",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.TextBlock(
                                                label="Naslov", required=False
                                            ),
                                        ),
                                        (
                                            "points",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.field_block.TextBlock,
                                                label="Točka",
                                                min=1,
                                            ),
                                        ),
                                    ],
                                    label="Modul s točkami",
                                ),
                            ),
                            (
                                "description",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.TextBlock(
                                                label="Naslov", required=False
                                            ),
                                        ),
                                        (
                                            "description",
                                            wagtail.blocks.TextBlock(label="Opis"),
                                        ),
                                    ],
                                    label="Modul z opisom",
                                ),
                            ),
                            (
                                "specifications",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "title",
                                            wagtail.blocks.TextBlock(
                                                label="Naslov", required=False
                                            ),
                                        ),
                                        (
                                            "points",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "name",
                                                            wagtail.blocks.TextBlock(
                                                                label="Specifikacije"
                                                            ),
                                                        ),
                                                        (
                                                            "value",
                                                            wagtail.blocks.TextBlock(
                                                                label="Vrednost"
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                                label="Specifikacije",
                                                min=1,
                                            ),
                                        ),
                                    ],
                                    label="Modul s specifikacijami",
                                ),
                            ),
                        ],
                        blank=True,
                        null=True,
                        use_json_field=True,
                        verbose_name="Moduli",
                    ),
                ),
                (
                    "tag",
                    models.CharField(
                        blank=True,
                        max_length=16,
                        null=True,
                        verbose_name="Oznaka na kartici",
                    ),
                ),
                (
                    "prima_location_id",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Prima location id"
                    ),
                ),
                (
                    "prima_group_id",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Prima group id"
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="home.customimage",
                        verbose_name="Slika",
                    ),
                ),
                (
                    "meta_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="home.customimage",
                        verbose_name="Meta slika",
                    ),
                ),
                (
                    "required_workshop",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="home.workshop",
                        verbose_name="Zahteva usposabljanje?",
                    ),
                ),
                (
                    "thumbnail",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="home.customimage",
                        verbose_name="Predogledna slika",
                    ),
                ),
            ],
            options={
                "verbose_name": "Delovna postaja",
                "verbose_name_plural": "Delovne postaje",
            },
            bases=("wagtailcore.page",),
        ),
    ]
