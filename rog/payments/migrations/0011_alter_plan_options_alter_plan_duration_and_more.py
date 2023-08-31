# Generated by Django 4.1.10 on 2023-08-29 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_alter_plan_pantheon_ident_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={'verbose_name': 'Plačilni paket', 'verbose_name_plural': 'Uporabniki - plačilni paketi'},
        ),
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.IntegerField(verbose_name='Koliko dni traja paket?'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='is_subscription',
            field=models.BooleanField(default=False, verbose_name='Je naročnina?'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='month_token_limit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Mesečna omejitev porabe žetonov'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(help_text='Npr. letna uporabnina', max_length=100, verbose_name='Ime paketa'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='price',
            field=models.IntegerField(verbose_name='Cena'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='tokens',
            field=models.IntegerField(default=0, verbose_name='Koliko žetonov dobi uporabnik?'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='week_token_limit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tedenska omejitev porabe žetonov'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='workshops',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Koliko delavnic dobi uporabnik v paketu?'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='year_token_limit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Letna omejitev porabe žetonov'),
        ),
        migrations.AddField(
            model_name='plan',
            name='discounted_price',
            field=models.IntegerField(default=10, help_text='Price for younger than 26 years old and older than 65', verbose_name='Discounted price'),
            preserve_default=False,
        ),
    ]
