# Generated by Django 3.1.5 on 2021-01-21 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_auto_20210121_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
    ]