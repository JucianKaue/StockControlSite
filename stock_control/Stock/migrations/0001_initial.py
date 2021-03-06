# Generated by Django 3.1.7 on 2021-03-12 13:02

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=50)),
                ('entry_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('brand', models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, to='Stock.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('clothes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Stock.clothes')),
            ],
        ),
    ]
