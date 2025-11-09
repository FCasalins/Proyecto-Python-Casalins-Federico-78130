from django.urls import path,include
from propiedades.views import propiedades

urlpatterns = [
    path("", propiedades , name="propiedades"),
    ]