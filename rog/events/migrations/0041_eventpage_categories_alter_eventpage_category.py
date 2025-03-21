# Generated by Django 4.2.15 on 2025-03-11 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0040_alter_eventpage_labs'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='event_pages', to='events.eventcategory', verbose_name='Kategorije'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_pages_old', to='events.eventcategory', verbose_name='Kategorija'),
        ),
    ]
