from django.urls import path

from . import views

urlpatterns = [
    path("", views.commision_view, name="index"),
]
