# Generated by Django 3.1.5 on 2021-01-31 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0011_auto_20210131_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='films', to='films.category'),
        ),
    ]
