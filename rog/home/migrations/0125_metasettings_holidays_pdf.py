# Generated by Django 4.2.15 on 2025-02-26 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0013_delete_uploadeddocument'),
        ('home', '0124_alter_tool_options_alter_toolspecification_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='metasettings',
            name='holidays_pdf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.document', verbose_name='PDF s prazni za trenutno leto'),
        ),
    ]
