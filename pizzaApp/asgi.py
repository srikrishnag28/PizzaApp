import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from home import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizzaApp.settings')

django_asgi_app = get_asgi_application()

ws_pattern = [
    path('ws/pizza/<order_id>', consumers.OrderProgress.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(
        ws_pattern
    ))
})