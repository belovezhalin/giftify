from decimal import Decimal, InvalidOperation
from django.test import TestCase
from store.models import Product
from store.decorators import SaleDecorator, SpecialOccasionDecorator

class DecoratorTestCase(TestCase):
    def setUp(self):
        self.product = Product(name="Test Product", price=Decimal('100.00'))

    def test_sale_decorator(self):
        discount = 10
        sale_decorator = SaleDecorator(self.product, discount)
        expected_price = Decimal('90.00')
        self.assertEqual(sale_decorator.sale_price, expected_price)

    def test_special_occasion_decorator(self):
        occasion = "Christmas"
        special_decorator = SpecialOccasionDecorator(self.product, occasion)
        expected_mark = "Special Occasion: Christmas"
        self.assertEqual(special_decorator.mark, expected_mark)

    def test_sale_decorator_invalid_discount(self):
        discount = -10
        with self.assertRaises(InvalidOperation):
            SaleDecorator(self.product, discount).sale_price

    def test_sale_decorator_high_discount(self):
        discount = 150
        with self.assertRaises(InvalidOperation):
            SaleDecorator(self.product, discount).sale_price

    def test_special_occasion_decorator_empty_occasion(self):
        occasion = ""
        special_decorator = SpecialOccasionDecorator(self.product, occasion)
        expected_mark = "Special Occasion: "
        self.assertEqual(special_decorator.mark, expected_mark)