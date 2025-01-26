from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from store.models import Customer, Product, Order, OrderItem
from django.contrib.auth.models import AnonymousUser
from store.utils import cookieCart, cartData, guestOrder
from decimal import Decimal
import json

class UtilsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='test@example.com')
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('100.00'),
            category=None,
            place='Test Place',
            discount=0,
            special_mark=''
        )

    def test_cookieCart_empty_cart(self):
        request = self.factory.get('/')
        request.COOKIES['cart'] = json.dumps({})
        response = cookieCart(request)
        self.assertEqual(response['cartItems'], 0)
        self.assertEqual(response['order']['get_cart_total'], 0)
        self.assertEqual(response['order']['get_cart_items'], 0)
        self.assertEqual(response['items'], [])

    def test_cookieCart_with_items(self):
        request = self.factory.get('/')
        request.COOKIES['cart'] = json.dumps({str(self.product.id): {'quantity': 2}})
        response = cookieCart(request)
        self.assertEqual(response['cartItems'], 2)
        self.assertEqual(response['order']['get_cart_total'], Decimal('200.00'))
        self.assertEqual(response['order']['get_cart_items'], 2)
        self.assertEqual(len(response['items']), 1)
        self.assertEqual(response['items'][0]['id'], self.product.id)

    def test_cartData_authenticated_user(self):
        request = self.factory.get('/')
        request.user = self.user
        response = cartData(request)
        self.assertEqual(response['cartItems'], 0)
        self.assertEqual(response['order'].customer, self.customer)
        self.assertEqual(response['items'], [])

    def test_cartData_unauthenticated_user(self):
        request = self.factory.get('/')
        request.COOKIES['cart'] = json.dumps({str(self.product.id): {'quantity': 2}})
        request.user = AnonymousUser()
        response = cartData(request)
        self.assertEqual(response['cartItems'], 2)
        self.assertEqual(response['order']['get_cart_total'], Decimal('200.00'))
        self.assertEqual(response['order']['get_cart_items'], 2)
        self.assertEqual(len(response['items']), 1)
        self.assertEqual(response['items'][0]['id'], self.product.id)

    def test_guestOrder(self):
        request = self.factory.get('/')
        request.COOKIES['cart'] = json.dumps({str(self.product.id): {'quantity': 2}})
        data = {'form': {'name': 'Guest', 'email': 'guest@example.com'}}
        customer, order = guestOrder(request, data)
        self.assertEqual(customer.name, 'Guest')
        self.assertEqual(customer.email, 'guest@example.com')
        self.assertEqual(order.customer, customer)
        self.assertEqual(order.complete, False)
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertEqual(order.orderitem_set.first().product, self.product)
        self.assertEqual(order.orderitem_set.first().quantity, 2)