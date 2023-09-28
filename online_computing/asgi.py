"""
ASGI config for online_computing project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

from math_computing import routing as math_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_computing.settings')

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            math_routing.websocket_urlpatterns
        )
    ),
    'http': get_asgi_application()
})
