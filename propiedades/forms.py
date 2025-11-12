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
    codigo = forms.IntegerField(
        required=False,
        label="Código de propiedad",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345'})
    )
    calle = forms.CharField(
        required=False,
        label="Calle",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: San Martín'})
    )

    class Meta:
        model = Propiedad
        fields = [
            "codigo", "calle",
            "operacion", "tipo", "localidad", "barrio", "ambientes", "precio_min", "precio_max"
        ]
        labels = {
            "operacion": "Operación",
            "tipo": "Tipo de Propiedad",
            "localidad": "Localidad",
            "barrio": "Barrio",
            "ambientes": "Ambientes",
        }
        widgets = {
            "operacion": forms.Select(attrs={'class': 'form-select'}),
            "tipo": forms.Select(attrs={'class': 'form-select'}),
            "localidad": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Chascomús'}),
            "barrio": forms.TextInput(attrs={'class': 'form-control'}),
            "ambientes": forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False