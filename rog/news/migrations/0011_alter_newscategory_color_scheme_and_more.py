# Generated by Django 4.1.9 on 2023-07-24 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_alter_newslistarchivepage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newscategory',
            name='color_scheme',
            field=models.CharField(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], default='light-gray', max_length=20),
        ),
        migrations.AlterField(
            model_name='newslistarchivepage',
            name='color_scheme',
            field=models.CharField(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], default='light-gray', max_length=20),
        ),
        migrations.AlterField(
            model_name='newslistpage',
            name='color_scheme',
            field=models.CharField(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], default='light-gray', max_length=20),
        ),
        migrations.AlterField(
            model_name='newspage',
            name='color_scheme',
            field=models.CharField(choices=[('brown', 'Rjava'), ('light-gray', 'Svetlo siva'), ('dark-gray', 'Temno siva'), ('light-blue', 'Svetlo modra'), ('dark-blue', 'Temno modra'), ('light-green', 'Svetlo zelena'), ('dark-green', 'Temno zelena'), ('dark-purple', 'Temno vijolična'), ('light-purple', 'Svetlo vijolična'), ('red', 'Rdeča'), ('beige', 'Bež'), ('beige-gray', 'Umazana siva'), ('orange', 'Oranžna'), ('pink', 'Roza'), ('yellow', 'Rumena'), ('white', 'Bela')], default='light-gray', max_length=20),
        ),
    ]
