"""
ASGI config for huawei_dj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huawei_dj.settings')
django.setup()


from commision.routing import ws_urlpatterns


asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})

    
