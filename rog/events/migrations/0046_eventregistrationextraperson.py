# Generated by Django 4.2.15 on 2025-04-02 08:43

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0045_alter_eventpage_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistrationExtraPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('person_name', models.TextField(verbose_name='Ime osebe')),
                ('person_surname', models.TextField(verbose_name='Priimek osebe')),
                ('event_registration', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registration_extra_people', to='events.eventregistration')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
