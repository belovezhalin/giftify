from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Customer, Category, Product, Order, OrderItem

class ModelsTestCase(TestCase):
    def setUp(self):
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
        self.order = Order.objects.create(customer=self.customer, complete=False, transaction_id='123456')
        self.order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

    def test_customer_str(self):
        self.assertEqual(str(self.customer), 'Test Customer')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Spa')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Spa Package')

    def test_product_sale_price(self):
        self.assertEqual(self.product.sale_price, Decimal('90.00'))

    def test_product_no_discount(self):
        product_no_discount = Product.objects.create(
            name='No Discount Product',
            price=Decimal('50.00'),
            category=self.category
        )
        self.assertIsNone(product_no_discount.sale_price)

    def test_product_special_occasion_mark(self):
        self.assertEqual(self.product.special_occasion_mark, 'Special Occasion: Special')

    def test_product_no_special_mark(self):
        product_no_special_mark = Product.objects.create(
            name='No Special Mark Product',
            price=Decimal('50.00'),
            category=self.category
        )
        self.assertIsNone(product_no_special_mark.special_occasion_mark)

    def test_order_str(self):
        self.assertEqual(str(self.order), str(self.order.id))

    def test_order_get_cart_total(self):
        self.assertEqual(self.order.get_cart_total, Decimal('200.00'))

    def test_order_get_cart_items(self):
        self.assertEqual(self.order.get_cart_items, 2)

    def test_order_no_items(self):
        empty_order = Order.objects.create(customer=self.customer, complete=False, transaction_id='654321')
        self.assertEqual(empty_order.get_cart_total, Decimal('0.00'))
        self.assertEqual(empty_order.get_cart_items, 0)

    def test_order_item_get_total(self):
        self.assertEqual(self.order_item.get_total, Decimal('200.00'))

    def test_order_item_zero_quantity(self):
        zero_quantity_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=0)
        self.assertEqual(zero_quantity_item.get_total, Decimal('0.00'))

    def test_order_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            OrderItem.objects.create(product=self.product, order=self.order, quantity=-2)

    def test_order_negative_cart_total(self):
        negative_price_product = Product.objects.create(
            name='Negative Price Product',
            price=Decimal('-50.00'),
            category=self.category
        )
        OrderItem.objects.create(product=negative_price_product, order=self.order, quantity=1)
        self.assertEqual(self.order.get_cart_total, Decimal('50.00'))