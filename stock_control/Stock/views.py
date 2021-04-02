from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.utils.safestring import mark_safe

from .models import *
from datetime import datetime


# Create your views here.
class FormEntry(forms.Form):
    code = forms.CharField(max_length=15, required=True)
    size = forms.CharField(max_length=3, required=True,
                           widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'}))
    description = forms.CharField(max_length=50, required=True,
                                  widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=True)
    entry_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)
    sell_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)

    amount = forms.IntegerField(min_value=0, initial=1, required=True)
    date = forms.DateTimeField(required=True)

    def formatted(self):
        return {'code': self.cleaned_data['code'],
                'size': f"{self.cleaned_data['size']}".upper(),
                'description': f"{self.cleaned_data['description']}".upper(),
                'brand': self.cleaned_data['brand'],
                'entry_price': self.cleaned_data['entry_price'],
                'sell_price': self.cleaned_data['sell_price'],
                'amount': self.cleaned_data['amount'],
                'date': self.cleaned_data['date']}


class FormSell(forms.Form):
    clothes = forms.ModelChoiceField(Inventory.objects.filter(amount__gt=0))
    amount = forms.IntegerField(min_value=1, initial=1, required=True)
    date = forms.DateTimeField(required=True)


def SEARCH(query, category, products_db, brand_db, search_db):
    if query:
        if category == 'CÓDIGO':
            products = []
            for clothes in products_db.objects.filter(code__icontains=query):
                for product in search_db.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'TAMANHO':
            products = []
            for clothes in products_db.objects.filter(size=query):
                for product in search_db.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'DESCRIÇÃO':
            products = []
            for clothes in products_db.objects.filter(description__icontains=query):
                for product in search_db.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'MARCA':
            products = []
            for brand in brand_db.objects.filter(name__icontains=query):
                for clothes in products_db.objects.filter(brand=brand):
                    for product in search_db.objects.filter(clothes=clothes):
                        products.append(product)
        elif category == 'PREÇO':
            products = []
            for clothes in products_db.objects.filter(sell_price=query):
                for product in search_db.objects.filter(clothes=clothes):
                    products.append(product)
        elif category == 'QUANTIDADE':
            products = search_db.objects.filter(amount=query)
        else:
            products = []
    else:
        products = search_db.objects.all()

    return products


def add_product(request):
    form = FormEntry(request.POST or None)
    form['date'].initial = datetime.now()
    if form.is_valid():
        form = form.formatted()
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

        return render(request, 'stock/add_product.html', {'form': FormEntry(initial={'date': datetime.now()}),
                                                          'page_title': 'Adicionar produto',
                                                          'title': 'Adiconar produto'})
    else:
        return render(request, 'stock/add_product.html', {'form': form,
                                                          'page_title': 'Adicionar produto',
                                                          'title': 'Adiconar produto'})


def add_existing_product(request, pk):
    product = Entry.objects.get(pk=pk)
    form = FormEntry(initial={
        'code': product.clothes.code,
        'size': product.clothes.size,
        'description': product.clothes.description,
        'brand': product.clothes.brand,
        'entry_price': product.clothes.entry_price,
        'sell_price': product.clothes.sell_price,
        'date': datetime.now(),
        'amount': 1
    })

    if request.method == 'POST':
        form = FormEntry(request.POST or None)
        if form.is_valid():
            form = form.formatted()
            # If the vesture already exists in the table clothes.
            if len(Clothes.objects.filter(code=form['code'], size=form['size'])) == 1:
                product = Clothes.objects.get(code=form['code'])
            else:
                product = Clothes(
                    code=form['code'],
                    size=form['size'],
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

            return render(request, 'stock/add_product.html', {'form': FormEntry(initial={'date': datetime.now()}),
                                                              'page_title': 'Adicionar produto',
                                                              'title': 'Adiconar produto'
                                                              })
    return render(request, 'Stock/add_product.html', {
        'form': form,
        'page_title': 'Adicionar produto',
        'title': 'Adiconar produto'
    })


def edit_product_entry(request, pk):
    product_entry = Entry.objects.get(pk=pk)
    if request.method == 'POST':
        form = FormEntry(request.POST or None)
        if form.is_valid():
            form = form.formatted()

            product = Clothes.objects.get(code=product_entry.clothes.code, size=product_entry.clothes.size)
            product_inventory = Inventory.objects.get(clothes=product)
            # Diminui a quantidade no estoque
            product_inventory.amount -= product_entry.amount   # Reset the product amount
            product_inventory.save()
            product_inventory = Inventory.objects.get(clothes=product)

            if product_entry.clothes.code != form['code'] or product_entry.clothes.size != form['size']:
                product_entry.delete()
                if product_inventory.amount == 0:
                    product_inventory.delete()
                    product.delete()

            # Update the product data
            query_clothes = Clothes.objects.filter(code=form['code'], size=form['size'])
            if len(query_clothes) == 1:
                vesture = query_clothes[0]
                vesture.description = form['description']
                vesture.brand = Brand.objects.get(name=form['brand'])
                vesture.entry_price = form['entry_price']
                vesture.sell_price = form['sell_price']
                vesture.save()
            elif len(query_clothes) == 0:
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
            product_entry.clothes = vesture
            product_entry.amount = form['amount']
            product_entry.save()

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
                'code': product_entry.clothes.code,
                'size': product_entry.clothes.size,
                'description': product_entry.clothes.description,
                'brand': product_entry.clothes.brand,
                'entry_price': product_entry.clothes.entry_price,
                'sell_price': product_entry.clothes.sell_price,
                'date': datetime.now(),
                'amount': product_entry.amount
            }),
            'page_title': 'Editar produto'
        })


def delete_product_entry(request, pk):
    product = Entry.objects.get(pk=pk)
    if request.method == 'POST':

        product_inventory = Inventory.objects.get(clothes=product.clothes)
        product_inventory.amount -= product.amount
        product_inventory.save()

        if product_inventory.amount == 0:
            product_inventory.delete()
            Clothes.objects.get(code=product.clothes.code, size=product.clothes.size).delete()

        product.delete()
        return redirect('table_inventory')
    else:
        return render(request, 'Stock/delete_product.html', {
            'product': product
        })


def table_inventory(request):
    query = request.GET.get("search")
    category = request.GET.get("category")

    products = SEARCH(query=query,
                      category=category,
                      products_db=Clothes,
                      brand_db=Brand,
                      search_db=Inventory)

    return render(request, 'stock/table_inventory.html', {
        'products': products
    })


def table_entry(request):
    query = request.GET.get("search")
    category = request.GET.get("category")

    products = SEARCH(query=query,
                      category=category,
                      products_db=Clothes,
                      brand_db=Brand,
                      search_db=Entry)

    return render(request, 'stock/table_entry.html', {
        'products': products
    })


def table_sales(request):
    query = request.GET.get("search")
    category = request.GET.get("category")

    products = SEARCH(query=query,
                      category=category,
                      products_db=Clothes,
                      brand_db=Brand,
                      search_db=Sales)

    return render(request, 'Stock/table_sales.html', {
        'products': products
    })


def sell_product(request, pk):
    form = FormSell(initial={
        'clothes': Clothes.objects.get(pk=pk),
        'amount': 1,
        'date': datetime.now()
    })
    if request.method == 'POST':
        form = FormSell(request.POST or None)
        if form.is_valid():
            form = form.cleaned_data
            vesture = Clothes.objects.get(pk=pk)

            # Add to sales table
            Sales(clothes=vesture,
                  amount=form['amount'],
                  date=form['date']).save()

            # Actualize the stock amount value
            product_inventory = Inventory.objects.get(clothes=vesture)
            product_inventory.amount -= form['amount']
            product_inventory.save()

            messages.success(request, f'"{vesture}" vendida com sucesso. ')

            return redirect('table_sales')

    return render(request, 'stock/add_product.html', {
        'title': 'VENDER PRODUTO',
        'form': form})
