from django.urls import path

from .consumers import GeneralConsumer
websocket_urlpatterns = [
    path('notifies/token=<str:token>', GeneralConsumer.as_asgi()),
]
