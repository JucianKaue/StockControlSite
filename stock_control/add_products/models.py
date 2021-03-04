from django.db import models
from django.utils import timezone


class Clothes(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    brand = models.CharField(max_length=15)
    size = models.CharField(max_length=3)
    cost_price = models.DecimalField(max_digits=5, decimal_places=2)
    sell_price = models.DecimalField(max_digits=5, decimal_places=2)


class Input(models.Model):
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name='input')
    date = models.DateField(timezone.now())
    amount = models.IntegerField()


class Stock(models.Model):
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name="stock")
    amount = models.IntegerField()
