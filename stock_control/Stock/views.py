from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django import forms
from .models import *
from django.utils import timezone


# Create your views here.
class FormEntry(forms.Form):
    code = forms.CharField(max_length=15, required=True)
    size = forms.CharField(max_length=3, required=True)
    description = forms.CharField(max_length=50, required=True)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=True)
    entry_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)
    sell_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)

    amount = forms.IntegerField(min_value=1, required=True)
    date = forms.DateTimeField(initial=timezone.now(), required=True)


def add_product(request):
    form = FormEntry(request.POST or None)
    if form.is_valid():
        form = form.cleaned_data
        # If the vesture already exists in the table clothes.
        if len(Clothes.objects.filter(code=form['code'], size=form['size'])) == 1:
            product = Clothes.objects.get(code=form['code'], size=form['size'])
        else:
            product = Clothes(
                code=form['code'],
                size=form['size'].upper(),
                description=form['description'],
                brand=Brand.objects.get(name='Daksul'),
                entry_price=form['entry_price'],
                sell_price=form['sell_price']
            )
            product.save()

        Entry(
            clothes=product,
            amount=form['amount'],
            date=form['date'],
            ).save()

        # Add to inventory
        query_inventory = Inventory.objects.filter(clothes=product)
        if len(query_inventory) == 1:
            amount = query_inventory[0].amount + product.amount
            query_inventory[0].amount += product.amount
            query_inventory[0].save()
        else:
            Inventory(
                clothes=product,
                amount=form['amount']
            ).save()

        messages.success(request, f'Produto "{product}" adicionado com sucesso')

        return render(request, 'stock/add_product.html', {'form': FormEntry()})
    return render(request, 'stock/add_product.html', {'form': form})


def table_inventory(request):
    query = request.GET.get("search")
    category = request.GET.get("category")

    if query:
        if category == 'CÓDIGO':
            products = []
            for clothes in Clothes.objects.filter(code=query):
                for product in Inventory.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'TAMANHO':
            products = []
            for clothes in Clothes.objects.filter(size=query):
                for product in Inventory.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'DESCRIÇÃO':
            products = []
            for clothes in Clothes.objects.filter(description=query):
                for product in Inventory.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'MARCA':
            products = []
            for clothes in Clothes.objects.filter(brand=query):
                for product in Inventory.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'PREÇO':
            products = []
            for clothes in Clothes.objects.filter(sell_price=query):
                for product in Inventory.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'QUANTIDADE':
            products = Inventory.objects.filter(amount=query)
    else:
        products = Inventory.objects.all()

    theaders = ['CÓDIGO', 'TAMANHO', 'DESCRIÇÃO', 'MARCA', 'PREÇO', 'QUANTIDADE']
    tdata = []
    for product in products:
        data_list = [
            product.clothes.code,
            product.clothes.size,
            product.clothes.description,
            product.clothes.brand,
            product.clothes.sell_price,
            product.amount,
        ]
        tdata.append(data_list)

    return render(request, 'stock/list_products.html', {
        'page_title': 'Tabela Estoque',
        'table_headers': theaders,
        'table_data': tdata
    })


def table_entry(request):
    query = request.GET.get("search")
    category = request.GET.get("category")

    if query:
        if category == 'CÓDIGO':
            products = []
            for clothes in Clothes.objects.filter(code=query):
                for product in Entry.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'TAMANHO':
            products = []
            for clothes in Clothes.objects.filter(size=query):
                for product in Entry.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'DESCRIÇÃO':
            products = []
            for clothes in Clothes.objects.filter(description=query):
                for product in Entry.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'MARCA':
            products = []
            for clothes in Clothes.objects.filter(brand=query):
                for product in Entry.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'PREÇO':
            products = []
            for clothes in Clothes.objects.filter(sell_price=query):
                for product in Entry.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'QUANTIDADE':
            products = Entry.objects.filter(amount=query)
        elif category == 'DATA':
            products = Entry.objects.filter(date__icontains=query)
    else:
        products = Entry.objects.all()

    theaders = ['CÓDIGO', 'TAMANHO', 'DESCRIÇÃO', 'MARCA', 'PREÇO', 'QUANTIDADE', 'DATA']
    tdata = []
    for product in products:
        data_list = [
            product.clothes.code,
            product.clothes.size,
            product.clothes.description,
            product.clothes.brand,
            product.clothes.sell_price,
            product.amount,
            product.date
        ]
        tdata.append(data_list)

    return render(request, 'stock/list_products.html', {
        'page_title': 'Tabela de entrada',
        'table_headers': theaders,
        'table_data': tdata,
    })



