from django.shortcuts import render, redirect
from .forms import *
from .models import Propiedad, Tasacion



def index(request):
    return render(request, "Inmobiliaria/index.html")



def propiedades(request):

    form = PropiedadForm(request.GET or None)
    propiedades = Propiedad.objects.filter(activo=True)

    if form.is_valid():
        operacion = form.cleaned_data.get('operacion')
        tipo = form.cleaned_data.get('tipo')
        localidad = form.cleaned_data.get('localidad')
        barrio = form.cleaned_data.get('barrio')
        ambientes = form.cleaned_data.get('ambientes')
        precio_min = form.cleaned_data.get('precio_min')
        precio_max = form.cleaned_data.get('precio_max')

        if operacion:
            propiedades = propiedades.filter(operacion=operacion)
        if tipo:
            propiedades = propiedades.filter(tipo=tipo)
        if localidad:
            propiedades = propiedades.filter(localidad__icontains=localidad)
        if barrio:
            propiedades = propiedades.filter(barrio__icontains=barrio)
        if ambientes:
            propiedades = propiedades.filter(ambientes=ambientes)
        if precio_min:
            propiedades = propiedades.filter(precio__gte=precio_min)
        if precio_max:
            propiedades = propiedades.filter(precio__lte=precio_max)

    return render(request, 'inmobiliaria/propiedades.html', {
        'form': form,
        'propiedades': propiedades,
    })



def tasaciones(request):
    if request.method == "POST":
        form = TasacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasaciones")
    else:
        form = TasacionForm()

    tasaciones = Tasacion.objects.all().order_by("-fecha_solicitud")
    return render(request, "inmobiliaria/tasaciones.html", {"form": form, "tasaciones": tasaciones})



def nosotros(request):
    return render(request, "inmobiliaria/nosotros.html")