from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<uuid:sujet_id>/', consumers.MessageConsumer.as_asgi()),
]
