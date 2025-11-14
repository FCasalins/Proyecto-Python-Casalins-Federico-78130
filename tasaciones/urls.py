from django.urls import path
from tasaciones.views import tasaciones

urlpatterns = [
    path("tasaciones", tasaciones, name="tasaciones"),
]