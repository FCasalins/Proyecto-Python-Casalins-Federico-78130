from django import forms
from Inmobiliaria.models import Propiedad
from Inmobiliaria.models import Tasacion
# from coder.models import tabla LLAMA A UNA CLASE DE LA BASE DE DATOS

class PropiedadForm(forms.ModelForm):
    precio_min = forms.DecimalField(
        required=False,
        label="Precio mínimo",
        min_value=0,
        decimal_places=2
    )
    precio_max = forms.DecimalField(
        required=False,
        label="Precio máximo",
        min_value=0,
        decimal_places=2
    )
    class Meta:
        model = Propiedad
        fields = ["codigo", "operacion", "tipo", "localidad", "barrio", "calle", "ambientes", "precio_min", "precio_max"]
    labels = {
        "operacion": "Operación",
        "tipo": "Tipo de Propiedad",
        "localidad": "Localidad",
        "barrio": "Barrio",
        "calle": "Calle",
        "ambientes": "Ambientes",
    }
    widgets = {
        "operacion": forms.Select(attrs={'class': 'form-select'}),
        "tipo": forms.Select(attrs={'class': 'form-select'}),
        "localidad": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Chascomús'}),
        "barrio": forms.TextInput(attrs={'class': 'form-control'}),
        "calle": forms.TextInput(attrs={'class': 'form-control'}),
        "ambientes": forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    }

class TasacionForm(forms.ModelForm):
    class Meta:
        model = Tasacion
        fields = [
            "cliente",
            "agente",
            "nombre",
            "email",
            "telefono",
            "localidad",
            "direccion",
            "tipo_propiedad",
            "superficie_total",
            "superficie_cubierta",
            "ambientes",
            "observaciones",
        ]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select", "placeholder": "Seleccionar cliente"}),
            "agente": forms.Select(attrs={"class": "form-select", "placeholder": "Seleccionar agente"}),
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del solicitante"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "ejemplo@correo.com"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono de contacto"}),
            "localidad": forms.TextInput(attrs={"class": "form-control", "placeholder": "Localidad"}),
            "direccion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dirección completa"}),
            "tipo_propiedad": forms.Select(
                choices=[
                    ("Casa", "Casa"),
                    ("Departamento", "Departamento"),
                    ("Terreno", "Terreno"),
                    ("Local Comercial", "Local Comercial"),
                    ("Oficina", "Oficina"),
                ],
                attrs={"class": "form-select"},
            ),
            "superficie_total": forms.NumberInput(attrs={"class": "form-control", "placeholder": "m² totales"}),
            "superficie_cubierta": forms.NumberInput(attrs={"class": "form-control", "placeholder": "m² cubiertos"}),
            "ambientes": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Comentarios adicionales"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cliente"].label = "Cliente (opcional)"
        self.fields["agente"].label = "Agente asignado"
        self.fields["tipo_propiedad"].label = "Tipo de propiedad"
        self.fields["superficie_total"].label = "Superficie total (m²)"
        self.fields["superficie_cubierta"].label = "Superficie cubierta (m²)"