from django.urls import path
from .views import *



urlpatterns = [
    path('add_product/', add_product, name='add_product'),

    path('edit_product_entry/<pk>', edit_product_entry, name='edit_product_entry'),
    path('delete_product_entry/<pk>', delete_product_entry, name='delete_product_entry'),

    path('table_inventory/', table_inventory, name='table_inventory'),
    path('table_entry/', table_entry, name='table_entry'),

    #path('delete_product_inventory/<pk>', delete_product_entry, name='delete_product_inventory'),



]
