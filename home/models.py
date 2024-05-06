from django.db import models
import string
from django.contrib.auth.models import User
import random
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.dispatch import receiver

# Create your models here.


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pizza')

    def __str__(self):
        return self.name


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


CHOICES = (
    ("Order Received", "Order Received"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("Oder Delivered", "Oder Delivered"),
)


class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, blank=True)
    amount = models.IntegerField(default=100)
    status = models.CharField(max_length=100, choices=CHOICES, default="Order Received")
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not len(self.order_id):
            self.order_id = random_string_generator()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_id

    def give_order_details(order_id):
        order = Order.objects.filter(order_id=order_id).first()
        data = {'order_id': order.order_id, 'amount': order.amount, 'status': order.status}
        order_status = order.status
        order_percentage = 0
        if order_status == 'Order Received':
            order_percentage = 20
        elif order_status == 'Baking':
            order_percentage = 40
        elif order_status == 'Baked':
            order_percentage = 60
        elif order_status == 'Out for delivery':
            order_percentage = 80
        else:
            order_percentage = 100
        data['percentage'] = order_percentage
        return data

@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {'order_id': instance.order_id, 'amount': instance.amount, 'status': instance.status}
        order_status = instance.status
        order_percentage = 0
        if order_status == 'Order Received':
            order_percentage = 20
        elif order_status == 'Baking':
            order_percentage = 40
        elif order_status == 'Baked':
            order_percentage = 60
        elif order_status == 'Out for delivery':
            order_percentage = 80
        else:
            order_percentage = 100
        data['percentage'] = order_percentage
        async_to_sync(channel_layer.group_send)(
            "order_%s" % instance.order_id, {
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )


