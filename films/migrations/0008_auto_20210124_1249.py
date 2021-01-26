# Generated by Django 3.1.5 on 2021-01-24 11:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_auto_20210123_1348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date_posted']},
        ),
        migrations.RemoveField(
            model_name='film',
            name='views_number',
        ),
        migrations.AddField(
            model_name='comment',
            name='date_posted',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
