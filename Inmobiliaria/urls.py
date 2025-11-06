from django.urls import path
from Inmobiliaria.views import index, propiedades, tasaciones, nosotros

urlpatterns = [
    path("", index, name="index"),
    path("propiedades/", propiedades , name="propiedades"),
    path("tasaciones/", tasaciones, name="tasaciones"),
    path("nosotros/", nosotros, name="nosotros"),
]