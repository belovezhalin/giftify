from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from .decorators import *
from .observers import Observer, Subject, UserObserver
from django.core.mail import send_mail

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name if self.name else self.user.username

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model, Subject):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    place = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    discount = models.FloatField(default=0, help_text="Discount percentage (0-100)")
    special_mark = models.CharField(max_length=200, null=True, blank=True, help_text="Special mark for the product")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.discount > 0:
            self.notify(f"New offer on {self.name}: {self.discount}% off!")

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
    
    @property
    def sale_price(self):
        if self.discount > 0:
            decorated_product = SaleDecorator(self, self.discount)
            return round(decorated_product.sale_price, 2)
        return None

    @property
    def special_occasion_mark(self):
        if self.special_mark:
            decorated_product = SpecialOccasionDecorator(self, self.special_mark)
            return decorated_product.mark
        return None

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
