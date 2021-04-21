def search(query, category, products_db, brand_db, search_db):
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