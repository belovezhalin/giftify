import json
from django.test import TestCase, Client
from django.urls import reverse
from store.models import *
from store.observers import UserObserver
from django.contrib.auth.models import User
from django.core import mail

class StoreTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Spa")
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name="Spa Package",
            price=100,
            category=self.category,
            place="New York"
        )

    def test_store_view(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')
        self.assertContains(response, self.product.name)

    def test_store_view_with_filters(self):
        response = self.client.get(reverse('store'), {'category': self.category.id, 'min_price': 50, 'max_price': 150, 'place': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_store_view_with_invalid_filters(self):
        response = self.client.get(reverse('store'), {'category': self.category.id, 'min_price': 200, 'max_price': 300, 'place': 'Los Angeles'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product.name)

    def test_store_view_with_category_filter(self):
        response = self.client.get(reverse('store'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_store_view_with_price_range_filter(self):
        response = self.client.get(reverse('store'), {'min_price': 50, 'max_price': 150})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_store_view_with_place_filter(self):
        response = self.client.get(reverse('store'), {'place': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_store_view_with_no_products(self):
        Product.objects.all().delete()
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product.name)

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Customer.objects.filter(user__username='newuser').exists())

    def test_register_view_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_login_view_invalid(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Should stay on the same page

    def test_logout_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after successful logout

    def test_store_view_with_search(self):
        response = self.client.get(reverse('store'), {'search': 'Spa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_store_view_with_search_no_results(self):
        response = self.client.get(reverse('store'), {'search': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product.name)

class ObserverTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.customer = Customer.objects.create(user=self.user)
        self.product = Product.objects.create(name='Test Product', price=100, discount=10)

    def test_user_observer_receives_notification(self):
        observer = UserObserver(self.customer)
        self.product.attach(observer)
        with self.assertLogs('django', level='INFO') as cm:
            self.product.save()
            self.assertIn('INFO:django:New offer on testuser: New offer on Test Product: 10% off!', cm.output)

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.customer = Customer.objects.create(user=self.user, email='testuser@example.com', name='Test User')
        self.product = Product.objects.create(name='Test Product', price=100)
        self.order = Order.objects.create(customer=self.customer, complete=False)
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

    def test_order_completion_sends_email(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('process_order'), json.dumps({
            'form': {
                'name': 'Test User',
                'email': 'testuser@example.com',
                'total': '100.00'
            }
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertTrue(self.order.complete)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Order Confirmation', mail.outbox[0].subject)
        self.assertIn('Thank you for your order, Test User!', mail.outbox[0].body)