# Generated by Django 3.1.7 on 2021-03-14 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0003_clothes_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='stock_uploaded',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('clothes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stock.clothes')),
            ],
        ),
    ]
