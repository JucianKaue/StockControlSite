from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import *
from datetime import datetime


# Create your views here.
class FormEntry(forms.Form):
    code = forms.CharField(max_length=15, required=True)
    size = forms.CharField(max_length=3, required=True)
    description = forms.CharField(max_length=50, required=True)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=True)
    entry_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)
    sell_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)

    amount = forms.IntegerField(min_value=0, initial=1, required=True)
    date = forms.DateTimeField(initial=datetime.now(), required=True)


def add_product(request):
    form = FormEntry(request.POST or None)
    if form.is_valid():
        form = form.cleaned_data
        # If the vesture already exists in the table clothes.
        if len(Clothes.objects.filter(code=form['code'])) == 1:
            product = Clothes.objects.get(code=form['code'])
            if product.size != form['size']:
                product.size = form['size']
        else:
            product = Clothes(
                code=form['code'],
                size=form['size'].upper(),
                description=form['description'],
                brand=Brand.objects.get(name=form['brand']),
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
            query_inventory[0].amount += form['amount']
            query_inventory[0].save()
        else:
            Inventory(
                clothes=product,
                amount=form['amount']
            ).save()

        messages.success(request, f'Produto "{product}" adicionado com sucesso')

        return render(request, 'stock/add_product.html', {'form': FormEntry()})
    return render(request, 'stock/add_product.html', {'form': form})


def add_existing_product(request, pk):
    product = Entry.objects.get(pk=pk)
    form = FormEntry(initial={
        'code': product.clothes.code,
        'size': product.clothes.size,
        'description': product.clothes.description,
        'brand': product.clothes.brand,
        'entry_price': product.clothes.entry_price,
        'sell_price': product.clothes.sell_price,
        'amount': 1
    })

    if request.method == 'POST':
        form = FormEntry(request.POST or None)
        if form.is_valid():
            form = form.cleaned_data
            # If the vesture already exists in the table clothes.
            if len(Clothes.objects.filter(code=form['code'])) == 1:
                product = Clothes.objects.get(code=form['code'])
                if product.size != form['size']:
                    product.size = form['size']
            else:
                product = Clothes(
                    code=form['code'],
                    size=form['size'].upper(),
                    description=form['description'],
                    brand=Brand.objects.get(name=form['brand']),
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
                query_inventory[0].amount += form['amount']
                query_inventory[0].save()
            else:
                Inventory(
                    clothes=product,
                    amount=form['amount']
                ).save()

            messages.success(request, f'Produto "{product}" adicionado com sucesso')

            return render(request, 'stock/add_product.html', {'form': FormEntry()})
    return render(request, 'Stock/add_product.html', {
        'form': form
    })


def edit_product_entry(request, pk):
    product = Entry.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormEntry(request.POST or None)
        if form.is_valid():
            form = form.cleaned_data

            # Diminui a quantidade no estoque
            product_inventory = Inventory.objects.get(
                clothes=Clothes.objects.get(
                    code=product.clothes.code,
                    size=product.clothes.size))
            product_inventory.amount -= product.amount   # Reset the product amount
            product_inventory.save()

            # Update the product data
            query_clothes = Clothes.objects.filter(code=form['code'], size=form['size'])
            if len(query_clothes) == 1:
                vesture = query_clothes[0]
                vesture.description = form['description']
                vesture.brand = Brand.objects.get(name=form['brand'])
                vesture.entry_price = form['entry_price']
                vesture.sell_price = form['sell_price']
                vesture.save()
            else:
                vesture = Clothes(
                    code=form['code'],
                    size=form['size'],
                    description=form['description'],
                    brand=Brand.objects.get(name=form['brand']),
                    entry_price=form['entry_price'],
                    sell_price=form['sell_price']
                )
                vesture.save()

            # Add to entry
            product.delete()
            Entry(
                clothes=vesture,
                amount=form['amount'],
                date=form['date']
            ).save()

            # Add to inventory
            Inventory(
                clothes=vesture,
                amount=form['amount'],
            ).save()

            # Delete de duplicated products
            query_inventory = Inventory.objects.filter(clothes=Clothes.objects.get(code=form['code'], size=form['size']))
            if len(query_inventory) > 1:
                amount = 0
                for i in range(0, len(query_inventory)):
                    amount += query_inventory[i].amount
                    if i == len(query_inventory)-1:
                        query_inventory[i].amount = amount
                        query_inventory[i].save()
                    else:
                        query_inventory[i].delete()

            # uptade the data to all of the products with this product code
            query_clothes = Clothes.objects.filter(code=form['code'])
            for clothes in query_clothes:
                clothes.description = form['description']
                clothes.brand = Brand.objects.get(name=form['brand'])
                clothes.entry_price = form['entry_price']
                clothes.sell_price = form['sell_price']
                clothes.save()

            return redirect('table_entry')
    else:
        return render(request, 'Stock/add_product.html', {
            'form': FormEntry(initial={
                'code': product.clothes.code,
                'size': product.clothes.size,
                'description': product.clothes.description,
                'brand': product.clothes.brand,
                'entry_price': product.clothes.entry_price,
                'sell_price': product.clothes.sell_price,
                'amount': product.amount
            })
        })


def delete_product_entry(request, pk):
    product = Entry.objects.get(pk=pk)
    if request.method == 'POST':

        product_inventory = Inventory.objects.get(clothes=product.clothes)
        product_inventory.amount -= product.amount
        product_inventory.save()

        if product_inventory.amount == 0:
            product_inventory.delete()

        product.delete()
        return redirect('table_inventory')
    else:
        return render(request, 'Stock/delete_product.html', {
            'product': product
        })


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
            products = []
    else:
        products = Inventory.objects.all()

    return render(request, 'stock/table_inventory.html', {
        'products': products
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
            products = []
    else:
        products = Entry.objects.all()

    return render(request, 'stock/table_entry.html', {
        'products': products
    })



