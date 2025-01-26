from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Customer, Category, Product, Order, OrderItem
from django.utils import timezone
from decimal import Decimal
import json

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='test@example.com')
        self.category1 = Category.objects.create(name='Spa')
        self.category2 = Category.objects.create(name='Fitness')
        self.product1 = Product.objects.create(
            name='Spa Package',
            price=100,
            category=self.category1,
            place='Warsaw',
            discount=10,
            special_mark='Special'
        )
        self.product2 = Product.objects.create(
            name='Fitness Package',
            price=150,
            category=self.category2,
            place='New York',
            discount=0,
            special_mark=''
        )
        self.order = Order.objects.create(customer=self.customer, complete=False, transaction_id='123456')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/register.html')

        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        
    def test_custom_logout_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('store'))

    def test_store_view(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_cart_view(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_checkout_view(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/checkout.html')

    def test_updateItem_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('update_item'), json.dumps({
            'productId': self.product.id,
            'action': 'add'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderItem.objects.get(order=self.order, product=self.product).quantity, 1)

    def test_processOrder_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('process_order'), json.dumps({
            'form': {
                'total': '100.00'
            }
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertTrue(self.order.complete)

    def test_store_view_with_category_filter(self):
        response = self.client.get(reverse('store'), {'category': self.category1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_store_view_with_multiple_categories(self):
        response = self.client.get(reverse('store'), {'category': [self.category1.id, self.category2.id]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_store_view_with_invalid_category(self):
        response = self.client.get(reverse('store'), {'category': 999})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_store_view_with_price_range_filter(self):
        response = self.client.get(reverse('store'), {'min_price': 50, 'max_price': 150})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)

    def test_store_view_with_place_filter(self):
        response = self.client.get(reverse('store'), {'place': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product2.name)

    def test_store_view_with_no_products(self):
        Product.objects.all().delete()
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product1.name)
        
    def test_subscribe_to_offers_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('subscribe_to_offers'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('store'))
        self.assertTrue(self.product._observers)