from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from propiedades.models import Propiedad
from propiedades.forms import PropiedadForm


class PropiedadListView(ListView):
    model = Propiedad
    template_name = "propiedades/propiedad_list.html"
    context_object_name = "propiedades"

    def get_queryset(self):
        queryset = Propiedad.objects.filter(activo=True)
        form = PropiedadForm(self.request.GET or None)

        # Si el usuario hizo una búsqueda (hay parámetros GET)
        if self.request.GET and form.is_valid():
            operacion = form.cleaned_data.get("operacion")
            tipo = form.cleaned_data.get("tipo")
            localidad = form.cleaned_data.get("localidad")
            barrio = form.cleaned_data.get("barrio")
            calle = form.cleaned_data.get("calle")
            codigo = form.cleaned_data.get("codigo")
            ambientes = form.cleaned_data.get("ambientes")
            precio_min = form.cleaned_data.get("precio_min")
            precio_max = form.cleaned_data.get("precio_max")

            # Aplicamos filtros solo si hay valores cargados
            if operacion:
                queryset = queryset.filter(operacion=operacion)
            if tipo:
                queryset = queryset.filter(tipo=tipo)
            if localidad:
                queryset = queryset.filter(localidad__icontains=localidad)
            if barrio:
                queryset = queryset.filter(barrio__icontains=barrio)
            if calle:
                queryset = queryset.filter(calle__icontains=calle)
            if codigo:
                queryset = queryset.filter(codigo=codigo)
            if ambientes:
                queryset = queryset.filter(ambientes=ambientes)
            if precio_min:
                queryset = queryset.filter(precio__gte=precio_min)
            if precio_max:
                queryset = queryset.filter(precio__lte=precio_max)

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
        "codigo", "operacion", "tipo", "descripcion", "localidad", "barrio",
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