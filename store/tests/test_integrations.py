from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Customer, Category, Product, Order, OrderItem
from decimal import Decimal
import json

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='test@example.com')
        self.category = Category.objects.create(name='Spa')
        self.product = Product.objects.create(
            name='Spa Package',
            price=Decimal('100.00'),
            category=self.category,
            place='Warsaw',
            discount=10,
            special_mark='Special'
        )

    def test_user_registration_and_login(self):
        # Test user registration
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Test user login
        response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_add_and_remove_from_cart(self):
        self.client.login(username='testuser', password='12345')

        # Add product to cart
        response = self.client.post(reverse('update_item'), json.dumps({
            'productId': self.product.id,
            'action': 'add'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.get(order__customer=self.customer, product=self.product).quantity, 1)

        # Remove product from cart
        response = self.client.post(reverse('update_item'), json.dumps({
            'productId': self.product.id,
            'action': 'remove'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.filter(order__customer=self.customer, product=self.product).count(), 0)

    def test_store_view_with_price_range_filter(self):
        response = self.client.get(reverse('store'), {'min_price': 50, 'max_price': 150})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_store_view_with_place_filter(self):
        response = self.client.get(reverse('store'), {'place': 'Warsaw'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_add_to_cart_and_checkout(self):
        self.client.login(username='testuser', password='12345')

        # Add product to cart
        response = self.client.post(reverse('update_item'), json.dumps({
            'productId': self.product.id,
            'action': 'add'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.get(order__customer=self.customer, product=self.product).quantity, 1)

        # Checkout
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/checkout.html')

        # Process order
        response = self.client.post(reverse('process_order'), json.dumps({
            'form': {
                'total': '100.00'
            }
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(customer=self.customer, complete=True)
        self.assertTrue(order.complete)

    def test_subscribe_to_offers(self):
        self.client.login(username='testuser', password='12345')

        # Subscribe to offers
        response = self.client.get(reverse('subscribe_to_offers'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('store'))

        # Check if the observer was attached to the product
        product = Product.objects.get(id=self.product.id)
        self.assertTrue(product._observers)