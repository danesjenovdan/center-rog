# Generated by Django 4.1.11 on 2023-12-06 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_alter_eventpage_number_of_places'),
        ('payments', '0034_paymentplanevent_delete_paymentplan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentplanevent',
            name='event',
        ),
        migrations.AddField(
            model_name='paymentplanevent',
            name='event_registration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_plans', to='events.eventregistration'),
        ),
        migrations.AddField(
            model_name='plan',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Plan'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek')], default='clanarina', max_length=20),
        ),
        migrations.AddField(
            model_name='promocode',
            name='payment_item_type',
            field=models.CharField(choices=[('clanarina', 'Plan'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek')], default='clanarina', max_length=20),
        ),
        migrations.AlterField(
            model_name='paymentplanevent',
            name='kind',
            field=models.CharField(choices=[('clanarina', 'Plan'), ('uporabnina', 'Uporabnina'), ('event', 'Dogodek')], default='clanarina', max_length=20),
        ),
    ]