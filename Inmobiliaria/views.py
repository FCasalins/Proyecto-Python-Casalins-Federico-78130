from django.shortcuts import render


def index(request):
    return render(request, "Inmobiliaria/index.html")


def nosotros(request):
    return render(request, "inmobiliaria/nosotros.html")