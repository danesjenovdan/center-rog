# Generated by Django 4.1.9 on 2023-07-01 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_userinterest_remove_user_link_user_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.ManyToManyField(to='users.userinterest', verbose_name='Kategorije zanimanj'),
        ),
    ]
