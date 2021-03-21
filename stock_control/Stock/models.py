from django.db import models
from django.utils import timezone


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=15, unique=True, null=False)

    def __str__(self):
        return f'{self.name}'


class Clothes(models.Model):
    code = models.CharField(max_length=15, null=False)
    size = models.CharField(max_length=3, null=False)
    description = models.CharField(max_length=50, null=False)
    brand = models.ForeignKey(Brand, on_delete=models.NOT_PROVIDED, null=False)
    entry_price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    sell_price = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    def __str__(self):
        return f'{self.code} - {self.size}| {self.description}'


class Entry(models.Model):
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(null=False)
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f'{self.clothes} --> Q:{self.amount} | D:{self.date}'


class Inventory(models.Model):
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
