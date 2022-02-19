import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')
django.setup()

from .middleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from social.apps.chat.routing import websocket_urlpatterns as chatts
from social.apps.general.routes import websocket_urlpatterns as genearl

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(chatts + genearl)
    )
})
