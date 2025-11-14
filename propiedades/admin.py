from django.contrib import admin
from .models import Propiedad, ImagenPropiedad


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ("codigo", "operacion", "tipo", "localidad", "activo")
    list_filter = ("operacion", "tipo", "localidad")
    search_fields = ("codigo", "localidad", "tipo")
    ordering = ("-fecha_publicacion",)

    fieldsets = (
        ("Información básica", {
            "fields": (
                "codigo",
                "operacion",
                "tipo",
                "estado",
                "descripcion",
                "imagen_principal",
                "activo",
            )
        }),
        ("Ubicación", {
            "fields": (
                "localidad",
                "barrio",
                "calle",
                "orientacion",
                "latitud",
                "longitud",
            )
        }),
        ("Dimensiones", {
            "fields": (
                "superficie_total",
                "superficie_cubierta",
                "ambientes",
                "dormitorios",
                "banios",
                "cochera",
            )
        }),
        ("Finanzas", {
            "fields": (
                "precio",
                "moneda",
            )
        }),
        ("Agente responsable", {
            "fields": ("agente",)
        }),
    )


@admin.register(ImagenPropiedad)
class ImagenPropiedadAdmin(admin.ModelAdmin):
    list_display = ("propiedad", "descripcion", "destacada")
    list_filter = ("destacada",)