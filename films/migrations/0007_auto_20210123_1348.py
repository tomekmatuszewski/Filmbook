# Generated by Django 3.1.5 on 2021-01-23 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0006_auto_20210122_1816"),
    ]

    operations = [
        migrations.RenameField(
            model_name="film",
            old_name="isPublic",
            new_name="isPrivate",
        ),
    ]
