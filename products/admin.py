from django.contrib import admin

# Register your models here.

# Здесь мы регистрируем таблицы нашей бд чтобы
# они отображались в админке

from products.models import ProductCategory, Product

admin.site.register(Product)
admin.site.register(ProductCategory)


