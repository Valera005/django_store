from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory
from users.models import User

# Create your views here. or controllers

# Здесь будут создаваться функции для отображения шаблонов
# на нашем сайте


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()

        category_id = self.kwargs.get("category_id")
        if category_id:
            return queryset.filter(category_id = category_id)

        return queryset


@login_required
def basket_add(request: WSGIRequest, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product = product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity = 1)
    else:
        basket = baskets.first()
        basket.quantity = basket.quantity + 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request: WSGIRequest, basket_id):
    basket = Basket.objects.get(id = basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def index(request):
#     context = {
#         'title': 'Test Title',
#     }
#
#     return render(request, 'products/index.html', context)

# def products(request, category_id = None, page_number = 1):
#
#     products_objects = Product.objects.filter(category_id = category_id) if category_id else Product.objects.all()
#
#     per_page = 3
#     paginator = Paginator(products_objects, per_page)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Store - Каталог',
#         'products' : products_paginator,
#         'categories': ProductCategory.objects.all()
#     }
#
#     return render(request,'products/products.html', context=context)
