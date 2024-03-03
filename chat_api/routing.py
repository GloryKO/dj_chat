# routing.py

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat_api.consumers import ChatConsumer
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app_backend.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
            ]
        )
    ),
})
