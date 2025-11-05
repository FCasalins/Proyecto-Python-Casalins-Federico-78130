from django.urls import path
from Inmobiliaria.views import index

urlpatterns = [
    path("", index, name="index"),
]