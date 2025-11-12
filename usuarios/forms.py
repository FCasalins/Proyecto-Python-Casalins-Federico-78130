from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from usuarios.models import Usuario


class UsuarioCreationForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('agente', 'Agente'),
        ('tasador', 'Tasador'),
    ]

    tipo_usuario = forms.ChoiceField(
        choices=TIPO_USUARIO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Tipo de usuario"
    )

    codigo_autorizacion = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Código de autorización (solo para agente o tasador)"
    )

    class Meta:
        model = Usuario
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "tipo_usuario",
            "codigo_autorizacion",
        )
        help_texts = {campo: "" for campo in fields}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        tipo_usuario = cleaned_data.get("tipo_usuario")
        codigo_autorizacion = cleaned_data.get("codigo_autorizacion")

        # Validación adicional para agentes o tasadores
        if tipo_usuario in ["agente", "tasador"]:
            CODIGO_VALIDO = "VALIDAR2025"  # ⚠️
            if codigo_autorizacion != CODIGO_VALIDO:
                raise forms.ValidationError(
                    "Código de autorización inválido. Solo el administrador puede registrar agentes o tasadores."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        tipo_usuario = self.cleaned_data.get("tipo_usuario")

        # Asigna el rol según la selección
        user.es_cliente = (tipo_usuario == "cliente")
        user.es_agente = (tipo_usuario == "agente")
        user.es_tasador = (tipo_usuario == "tasador")

        if commit:
            user.save()
        return user


class UsuarioChangeForm(UserChangeForm):
  
    # Formulario de edición de usuario.
    # - Para usuarios normales: permite editar solo datos personales.
    # - Para staff/admins: habilita campos extra de control (roles, activo, etc.).
  

    class Meta:
        model = Usuario
        fields = [
            "first_name",
            "last_name",
            "email",
            "avatar",
            "pais",
            "fecha_de_nacimiento",
            "direccion",
        ]
        widgets = {
            "fecha_de_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "pais": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si el usuario que edita es staff o superuser
        if user and user.is_staff:
            self.fields["activo"] = forms.BooleanField(
                required=False, label="Usuario activo"
            )
            self.fields["es_agente"] = forms.BooleanField(
                required=False, label="Agente"
            )
            self.fields["es_tasador"] = forms.BooleanField(
                required=False, label="Tasador"
            )
            self.fields["es_cliente"] = forms.BooleanField(
                required=False, label="Cliente"
            )
        
