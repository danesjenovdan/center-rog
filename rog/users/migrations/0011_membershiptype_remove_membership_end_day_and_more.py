# Generated by Django 4.1.9 on 2023-06-30 09:30

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_workshops_attended'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Ime članstva')),
                ('price', models.IntegerField(verbose_name='Cena')),
            ],
            options={
                'verbose_name': 'Tip članstva',
                'verbose_name_plural': 'Tipi članstva',
            },
        ),
        migrations.RemoveField(
            model_name='membership',
            name='end_day',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='start_day',
        ),
        migrations.AddField(
            model_name='membership',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membership',
            name='valid_from',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='valid_to',
            field=models.DateTimeField(blank=True, help_text='When the plan expires', null=True),
        ),
        migrations.CreateModel(
            name='MembershipTypeSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.TextField(verbose_name='Boniteta')),
                ('membership_type', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_specifications', to='users.membershiptype')),
            ],
            options={
                'verbose_name': 'Boniteta članstva',
                'verbose_name_plural': 'Bonitete članstva',
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.membershiptype'),
        ),
    ]