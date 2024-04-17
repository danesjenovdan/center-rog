# Generated by Django 4.1.11 on 2024-04-16 16:02

from django.db import migrations


def tag_user_gallery_images(apps, schema_editor):
    User = apps.get_model("users", "User")

    for user in User.objects.all():
        for image in user.gallery:
            image.value.tags.add("__user_gallery__")


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0036_membership_extended_by"),
    ]

    operations = [
        migrations.RunPython(
            tag_user_gallery_images, reverse_code=migrations.RunPython.noop
        ),
    ]