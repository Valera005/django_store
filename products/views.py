from django.shortcuts import render

from products.models import Product, ProductCategory


# Create your views here. or controllers

# Здесь будут создаваться функции для отображения шаблонов
# на нашем сайте


def index(request):
    context = {
        'title': 'Test Title',
    }

    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories' : ProductCategory.objects.all()
    }

    return render(request, 'products/products.html', context=context)
