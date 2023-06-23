from django.urls import path

from .consumers import RunCommandsOnNE

ws_urlpatterns = [
    path("ws/checkne/", RunCommandsOnNE.as_asgi())
]
