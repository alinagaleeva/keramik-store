from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Product


class IndexViewTestCase(TestCase):

    def test_index_view(self):
        path = reverse('home')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Keramik')
        self.assertTemplateUsed(response, 'main/index.html')


class AboutViewTestCase(TestCase):

    def test_about_view(self):
        path = reverse('about')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'about')
        self.assertTemplateUsed(response, 'main/about.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['goods.json']

    def test_products_list(self):
        path = reverse('shop')
        response = self.client.get(path)

        products = Product.objects.all()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'shop')
        self.assertTemplateUsed(response, 'main/shop.html')
        self.assertEqual(list(response.context_data['object_list']), list(products))


class PlateListViewTestCase(TestCase):
    fixtures = ['goods.json']

    def test_plate_page_view(self):
        product = Product.objects.first()
        path = reverse('plate_page', kwargs={'product_id': product.id})
        response = self.client.get(path)

        name = Product.objects.filter(id=product.id).first().name.lower()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], name)
        self.assertTemplateUsed(response, 'main/plate_page.html')
        self.assertEqual(
            response.context_data['product'],
            product
        )


'''class BagViewTestCase(TestCase):

    def test_bag_view(self):
        path = reverse('bag')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'bag')
        self.assertTemplateUsed(response, 'main/bag.html')'''

'''class ShippingViewTestCase(TestCase):

    def test__shipping_view(self):
        path = reverse('shipping')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'shipping')
        self.assertTemplateUsed(response, 'main/shipping.html')'''
