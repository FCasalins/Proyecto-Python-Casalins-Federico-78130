from django.shortcuts import render
from propiedades.forms import *
from propiedades.models import Propiedad

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