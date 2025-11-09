from django import forms
from propiedades.models import Propiedad

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