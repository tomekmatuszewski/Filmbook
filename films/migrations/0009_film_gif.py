# Generated by Django 3.1.5 on 2021-01-28 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0008_auto_20210126_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='gif',
            field=models.FileField(blank=True, upload_to='gifs'),
        ),
    ]
