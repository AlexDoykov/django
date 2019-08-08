# Generated by Django 2.2.4 on 2019-08-08 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0020_auto_20190808_1141'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='exchangerate',
            constraint=models.UniqueConstraint(fields=('valid_date', 'currency'), name='unique_fx_for_the_day'),
        ),
    ]