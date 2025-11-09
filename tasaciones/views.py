from django.shortcuts import render, redirect
from tasaciones.forms import *
from tasaciones.models import Tasacion


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