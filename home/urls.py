from django.urls import path, include
from django.shortcuts import HttpResponse
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('add/<int:pizza_id>', order_pizza, name='order_pizza'),
    path('order/<str:order_id>/', order, name='order')
]
