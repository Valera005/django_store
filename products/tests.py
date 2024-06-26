import os
from http import HTTPStatus

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'store.settings'
django.setup()

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory
from users.models import User


# Create your tests here.

class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse("index")
        response = self.client.get(path)

        print(response)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(response.context_data['title'], "Store")
        self.assertTemplateUsed("products/index.html", response)


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self) -> None:
        self.products = Product.objects.all()


    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)


        self.assertEqual(HTTPStatus.OK, response.status_code)
        # self.assertTemplateUsed(response, "products/products.html")
        self.assertEqual(response.context_data['title'], "Store - Каталог")
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))
        print("ok")


    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={"category_id": 1})
        response = self.client.get(path)


        self.assertEqual(HTTPStatus.OK, response.status_code)
        # self.assertTemplateUsed("products/products.html", response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )


