# Generated by Django 3.1.7 on 2021-03-26 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0004_auto_20210314_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='stock_uploaded',
        ),
        migrations.AlterField(
            model_name='entry',
            name='clothes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entry', to='Stock.clothes'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='clothes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='Stock.clothes'),
        ),
    ]
