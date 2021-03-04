from django.shortcuts import render
from django import forms
from django.utils import timezone

from .models import Clothes, Input, Stock


class DateInput(forms.DateInput):
    input_type = 'date'


class FormAddProducts(forms.Form):
    code = forms.CharField(label="Código",
                           max_length="10",
                           min_length="1",
                           widget=forms.TextInput(attrs={'placeholder': "código"}))
    desc = forms.CharField(label="Descrição",
                           widget=forms.TextInput(attrs={'placeholder': "descrição",
                                                         'id': "descricao"}))
    brand = forms.CharField(label="Marca",
                            max_length="15",
                            widget=forms.TextInput(attrs={'placeholder': "marca"}))
    size = forms.CharField(label="Tamanho",
                           max_length="3",
                           widget=forms.TextInput(attrs={'placeholder': "tamanho"}))
    cost_price = forms.DecimalField(label="Preço de custo",
                                    max_digits=5, decimal_places=2,
                                    widget=forms.TextInput(attrs={'placeholder': "preço de custo"}))
    sell_price = forms.DecimalField(label="Preço de venda",
                                    max_digits=5, decimal_places=2,
                                    widget=forms.TextInput(attrs={'placeholder': "preço de venda"}))
    date = forms.DateField(initial=timezone.now(),
                           widget=DateInput)
    amount = forms.IntegerField(label="Quantidade",
                                min_value=1,
                                widget=forms.TextInput(attrs={'value': 1}))


# Create your views here.
def index(request):

    if request.method == 'POST':
        form = FormAddProducts(request.POST)
        if form.is_valid():
            form_clean = form.cleaned_data
            product = Clothes()

            # if already exists a vesture in the database.
            if not len(Clothes.objects.filter(code=f"{form_clean['code']}", size=f"{form_clean['size']}")) == 0:

                product = Clothes.objects.get(code=f"{form_clean['code']}", size=f"{form_clean['size']}")

            else:
                product.code = form_clean['code']
                product.description = form_clean['desc']
                product.brand = form_clean['brand']
                product.size = form_clean['size']
                product.cost_price = float(form_clean['cost_price'])
                product.sell_price = float(form_clean['sell_price'])

            product.amount = int(form_clean['amount'])
            product.save()

            entry = Input(clothes=product, date=form.cleaned_data['date'], amount=form.cleaned_data['amount'])
            entry.save()

            # If the vesture not exists in stock table
            if len(Stock.objects.filter(clothes=entry.clothes)) == 0:
                Stock(clothes=entry.clothes, amount=product.amount).save()
            # IF the vesture exists in stock table
            else:
                stock_vesture = Stock.objects.get(clothes=entry.clothes)
                stock_vesture.amount = stock_vesture.amount + product.amount
                stock_vesture.save()

            return render(request, "add_products/index.html", {
                'form': FormAddProducts(),
                'products': Input.objects.filter(date=timezone.now())
            })

    return render(request, "add_products/index.html", {
        'form': FormAddProducts(),
        'products': Input.objects.filter(date=timezone.now())
    })
