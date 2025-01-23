from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .utils import cookieCart
from .utils import cookieCart, cartData, guestOrder
from .decorators import SaleDecorator, SpecialOccasionDecorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
import json
import datetime
from django.db.models import Min, Max

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            login(request, user)
            return redirect("store")
    else:
        form = UserCreationForm()
    return render(request, "store/register.html", {"form": form})

def custom_logout(request):
    logout(request)
    return redirect('store')

def store(request):
    if request.user.is_authenticated and not hasattr(request.user, 'customer'):
        Customer.objects.create(user=request.user)

    categories = Category.objects.all()
    products = Product.objects.all()

    min_price_value = products.aggregate(Min('price'))['price__min'] or 0
    max_price_value = products.aggregate(Max('price'))['price__max'] or 1000

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    place = request.GET.get('place')
    if place:
        products = products.filter(place__icontains=place)

    decorated_products = []
    for product in products:
        if product.price > 100:  # Example condition for sale
            product = SaleDecorator(product, 10)  # 10% discount
        if "special" in product.name.lower():  # Example condition for special occasion
            product = SpecialOccasionDecorator(product, "Special Occasion")
        decorated_products.append(product)

    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        "products": products,
        "cartItems": cartItems,
        "categories": categories,
        "min_price_value": min_price_value,
        "max_price_value": max_price_value,
    }

    return render(request, "store/store.html", context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if request.user.is_authenticated:
        if not hasattr(request.user, 'customer'):
            Customer.objects.create(user=request.user)

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("Action:", action)
    print("Product:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if(orderItem.quantity <= 0):
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        guestOrder(request, data)
     
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    return JsonResponse("Payment submitted...", safe=False)
