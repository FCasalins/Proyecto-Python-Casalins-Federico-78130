from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from propiedades.models import Propiedad, ImagenPropiedad
from propiedades.forms import PropiedadForm, ImagenPropiedadForm
from django.contrib.auth.decorators import login_required


class PropiedadListView(ListView):
    model = Propiedad
    template_name = "propiedades/propiedad_list.html"
    context_object_name = "propiedades"

    def get_queryset(self):
        queryset = Propiedad.objects.filter(activo=True)
        form = PropiedadForm(self.request.GET or None)

        if form.is_valid():
            data = form.cleaned_data

            if data.get("operacion"):
                queryset = queryset.filter(operacion=data["operacion"])
            if data.get("tipo"):
                queryset = queryset.filter(tipo=data["tipo"])
            if data.get("localidad"):
                queryset = queryset.filter(localidad__icontains=data["localidad"])
            if data.get("barrio"):
                queryset = queryset.filter(barrio__icontains=data["barrio"])
            if data.get("calle"):
                queryset = queryset.filter(calle__icontains=data["calle"])
            if data.get("codigo") not in (None, ""):
                queryset = queryset.filter(codigo=data["codigo"])
            if data.get("ambientes"):
                queryset = queryset.filter(ambientes=data["ambientes"])
            if data.get("precio_min") is not None:
                queryset = queryset.filter(precio__gte=data["precio_min"])
            if data.get("precio_max") is not None:
                queryset = queryset.filter(precio__lte=data["precio_max"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PropiedadForm(self.request.GET or None)
        return context

class PropiedadDetailView(DetailView):
    model = Propiedad
    template_name = "propiedades/propiedad_detail.html"
    context_object_name = "propiedad"


# --- SOLO PARA AGENTES ---
class SoloAgenteMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin que permite acceso sólo a usuarios con rol de agente."""

    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, "es_agente", False)

    def handle_no_permission(self):
        messages.error(self.request, "No tenés permisos para acceder a esta sección.")
        return super().handle_no_permission()


class PropiedadCreateView(SoloAgenteMixin, CreateView):
    model = Propiedad
    fields = [
        "operacion", "tipo", "descripcion", "localidad", "barrio",
        "calle", "superficie_total", "superficie_cubierta", "ambientes",
        "dormitorios", "banios", "cochera", "precio", "moneda",
        "estado", "imagen_principal", "activo"
    ]
    template_name = "propiedades/propiedad_create.html"
    success_url = reverse_lazy("propiedad_list")

    def form_valid(self, form):
        form.instance.agente = self.request.user
        messages.success(self.request, "Propiedad creada correctamente.")
        return super().form_valid(form)


class PropiedadUpdateView(SoloAgenteMixin, UpdateView):
    model = Propiedad
    fields = [
        "codigo", "operacion", "tipo", "descripcion", "localidad", "barrio",
        "calle", "superficie_total", "superficie_cubierta", "ambientes",
        "dormitorios", "banios", "cochera", "precio", "moneda",
        "estado", "imagen_principal", "activo"
    ]
    template_name = "propiedades/propiedad_update.html"
    success_url = reverse_lazy("propiedad_list")

    def form_valid(self, form):
        messages.success(self.request, "Propiedad actualizada correctamente.")
        return super().form_valid(form)

    def test_func(self):
        """Solo el agente propietario o superusuario puede editar."""
        propiedad = self.get_object()
        return self.request.user.is_superuser or self.request.user == propiedad.agente


class PropiedadDeleteView(SoloAgenteMixin, DeleteView):
    model = Propiedad
    template_name = "propiedades/propiedad_delete.html"
    success_url = reverse_lazy("propiedad_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Propiedad eliminada correctamente.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        propiedad = self.get_object()
        return self.request.user.is_superuser or self.request.user == propiedad.agente
    
@login_required
def agregar_imagenes(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)

    # Solo el agente dueño puede agregar imágenes
    if not request.user.es_agente or request.user != propiedad.agente:
        return redirect("propiedad_detail", pk=pk)

    if request.method == "POST":
        form = ImagenPropiedadForm(request.POST, request.FILES)

        if form.is_valid():
            imagenes = request.FILES.getlist("imagen")
            descripcion = form.cleaned_data.get("descripcion", "")

            for img in imagenes:
                ImagenPropiedad.objects.create(
                    propiedad=propiedad,
                    imagen=img,
                    descripcion=descripcion
                )

            return redirect("propiedad_detail", pk=pk)

    else:
        form = ImagenPropiedadForm()

    return render(request, "propiedades/propiedad_agregar_imagenes.html", {
        "form": form,
        "propiedad": propiedad,
    })