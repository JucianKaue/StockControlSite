from django.urls import path
from .views import *

urlpatterns = [
    path('add_product/', add_product, name='add_product'),
    path('table_inventory/', table_inventory, name='table_inventory'),
]
