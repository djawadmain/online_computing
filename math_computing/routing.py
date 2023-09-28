from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/math_computing/', consumers.MathComputing.as_asgi()),
]
