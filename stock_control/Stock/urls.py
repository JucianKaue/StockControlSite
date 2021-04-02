from django.urls import path
from .views import *


urlpatterns = [
    path('add_product/', add_product, name='add_product'),

    # Actions from entry table page
    path('add_existing_product/<pk>', add_existing_product, name='add_existing_product'),
    path('edit_product_entry/<pk>', edit_product_entry, name='edit_product_entry'),
    path('delete_product_entry/<pk>', delete_product_entry, name='delete_product_entry'),

    # Tables
    path('table_inventory/', table_inventory, name='table_inventory'),
    path('table_entry/', table_entry, name='table_entry'),
    path('table_sales/', table_sales, name='table_sales'),

    # Actions from sales table page
    path('sell_product/<pk>', sell_product, name='sell_product'),
    path('edit_product_sell/<pk>', edit_product_sell, name='edit_product_sell'),
    path('delete_product_sell/<pk>', delete_product_sell, name='delete_product_sell')



]
