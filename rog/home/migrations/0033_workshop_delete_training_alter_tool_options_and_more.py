# Generated by Django 4.1.9 on 2023-06-28 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_alter_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Ime usposabljanja')),
            ],
            options={
                'verbose_name': 'Usposabljanje',
                'verbose_name_plural': 'Usposabljanja',
            },
        ),
        migrations.DeleteModel(
            name='Training',
        ),
        migrations.AlterModelOptions(
            name='tool',
            options={'verbose_name': 'Orodje', 'verbose_name_plural': 'Orodja'},
        ),
        migrations.AlterModelOptions(
            name='toolspecification',
            options={'verbose_name': 'Specifikacija orodja', 'verbose_name_plural': 'Specifikacije orodja'},
        ),
        migrations.AddField(
            model_name='tool',
            name='required_workshop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.workshop', verbose_name='Zahteva usposabljanje?'),
        ),
    ]
