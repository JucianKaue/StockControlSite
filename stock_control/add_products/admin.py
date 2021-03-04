from django.contrib import admin

from .models import Clothes, Input, Stock


# Register your models here.
class ClothesAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "brand", "size", "cost_price", "sell_price")


admin.site.register(Clothes)
admin.site.register(Input)
admin.site.register(Stock)
