from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "es_agente",
        "es_tasador",
        "es_cliente",
    )
    list_filter = (
        "username",
        "last_name",
        "first_name",
    )

    list_display_links = (
        "username",
        "last_name",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Datos personales"), {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "avatar",
                "pais",
                "fecha_de_nacimiento",
                "direccion",
            )
        }),
        (_("Roles internos"), {
            "fields": (
                "es_agente",
                "es_tasador",
                "es_cliente",
            )
        }),
        (_("Permisos"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (_("Fechas importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "is_active",
                "is_staff",
                "is_superuser",
                "es_agente",
                "es_tasador",
                "es_cliente",
            ),
        }),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username", "last_name", "first_name")