# Generated by Django 3.1.5 on 2021-01-28 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0010_auto_20210128_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='poster',
            field=models.ImageField(blank=True, upload_to='posters'),
        ),
    ]