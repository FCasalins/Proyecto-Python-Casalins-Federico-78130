from django.urls import path
from propiedades.views import (
    PropiedadListView,
    PropiedadDetailView,
    PropiedadCreateView,
    PropiedadUpdateView,
    PropiedadDeleteView,
)

urlpatterns = [
    path("", PropiedadListView.as_view(), name="propiedad_list"),
    path("<int:pk>/", PropiedadDetailView.as_view(), name="propiedad_detail"),
    path("crear/", PropiedadCreateView.as_view(), name="propiedad_create"),
    path("<int:pk>/editar/", PropiedadUpdateView.as_view(), name="propiedad_update"),
    path("<int:pk>/eliminar/", PropiedadDeleteView.as_view(), name="propiedad_delete"),
]