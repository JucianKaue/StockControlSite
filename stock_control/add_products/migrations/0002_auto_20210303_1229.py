# Generated by Django 3.1.6 on 2021-03-03 15:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('add_products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input',
            name='date',
            field=models.DateField(verbose_name=datetime.datetime(2021, 3, 3, 15, 29, 27, 359461, tzinfo=utc)),
        ),
    ]