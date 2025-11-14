from django.shortcuts import render
from propiedades.models import Propiedad

def index(request):
    propiedades_destacadas = Propiedad.objects.filter(activo=True).order_by('-fecha_publicacion')[:3]

    return render(request, "inmobiliaria/index.html", {
        "propiedades_destacadas": propiedades_destacadas
    })
    return render(request, "Inmobiliaria/index.html")


def nosotros(request):
    return render(request, "inmobiliaria/nosotros.html")