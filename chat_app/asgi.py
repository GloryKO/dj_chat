# asgi.py

import os
from django.core.asgi import get_asgi_application
from chat_api.routing import application as chat_api_application
from channels.routing import ProtocolTypeRouter  # Import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": chat_api_application,  # Use the imported application from routing.py
})
