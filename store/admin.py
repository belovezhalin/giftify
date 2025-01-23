from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'place', 'discount', 'special_mark')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    fields = ('name', 'price', 'category', 'image', 'place', 'discount', 'special_mark')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
