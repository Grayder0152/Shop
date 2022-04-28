from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    re_path('ws/status/', consumers.StatusConsumer.as_asgi()),
    re_path('ws/registration/', consumers.RegistrationConsumer.as_asgi()),

]
