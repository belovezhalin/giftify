from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store import views
from django.contrib.auth import views as auth_views

class UrlsTestCase(SimpleTestCase):
    def test_store_url(self):
        url = reverse('store')
        self.assertEqual(resolve(url).func, views.store)

    def test_cart_url(self):
        url = reverse('cart')
        self.assertEqual(resolve(url).func, views.cart)

    def test_checkout_url(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, views.checkout)

    def test_update_item_url(self):
        url = reverse('update_item')
        self.assertEqual(resolve(url).func, views.updateItem)

    def test_process_order_url(self):
        url = reverse('process_order')
        self.assertEqual(resolve(url).func, views.processOrder)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.custom_logout)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_subscribe_to_offers_url(self):
        url = reverse('subscribe_to_offers')
        self.assertEqual(resolve(url).func, views.subscribe_to_offers)