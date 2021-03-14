from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django import forms
from .models import *
from datetime import date


# Create your views here.
class FormEntry(forms.Form):
    code = forms.CharField(max_length=15, required=True)
    size = forms.CharField(max_length=3, required=True)
    description = forms.CharField(max_length=50, required=True)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=True)
    entry_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)
    sell_price = forms.DecimalField(max_digits=6, decimal_places=2, required=True)

    amount = forms.IntegerField(min_value=1, required=True)
    date = forms.DateTimeField(initial=date.today(), required=True)


def add_product(request):
    form = FormEntry(request.POST or None)
    if form.is_valid():
        form = form.cleaned_data

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
            date=form['date']
            ).save()
        messages.success(request, 'Produto adicionado com sucesso')

        return render(request, 'stock/add_product.html', {'form': FormEntry()})
    return render(request, 'stock/add_product.html', {'form': form})


def list_products(request):
    pass