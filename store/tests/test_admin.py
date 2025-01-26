from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from store import admin
from store.models import Product, Category
from store.admin import ProductAdmin

class MockRequest:
    pass

class ProductAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.product_admin = ProductAdmin(Product, self.site)
        self.category = Category.objects.create(name="Spa")
        self.product = Product.objects.create(
            name="Spa Package",
            price=100,
            category=self.category,
            place="Warsaw",
            discount=10,
            special_mark="Special"
        )

    def test_list_display(self):
        self.assertEqual(
            self.product_admin.list_display,
            ('name', 'price', 'category', 'place', 'discount', 'special_mark')
        )

    def test_list_filter(self):
        self.assertEqual(self.product_admin.list_filter, ('category',))

    def test_search_fields(self):
        self.assertEqual(self.product_admin.search_fields, ('name', 'category__name'))

    def test_fields(self):
        self.assertEqual(
            self.product_admin.fields,
            ('name', 'price', 'category', 'image', 'place', 'discount', 'special_mark')
        )

    def test_category_registered(self):
        self.assertTrue(admin.site.is_registered(Category))

    def test_product_registered(self):
        self.assertTrue(admin.site.is_registered(Product))