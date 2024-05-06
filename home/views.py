from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def home(request):
    pizza = Pizza.objects.all()
    orders = Order.objects.filter(user=request.user.id)
    context = {'pizza': pizza, 'orders': orders}
    return render(request, 'home/index.html', context)


def order(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()
    if order is None:
        return redirect('/')
    context = {'order': order}
    return render(request, 'home/order.html', context)


def order_pizza(request, pizza_id):
    user = request.user
    pizza = Pizza.objects.get(id=pizza_id)
    order = Order(user=user, pizza=pizza, amount=pizza.price)
    order.save()
    return redirect('home')

