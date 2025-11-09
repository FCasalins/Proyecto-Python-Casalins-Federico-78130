from django.db import models
from django.contrib.auth.models import AbstractUser

def avatar_upload_to (instance, filename):
    return f"avatars/{instance.username}/{filename}"

class Usuario(AbstractUser):
    avatar = models.ImageField(
        upload_to = avatar_upload_to,
        default = "default/avatar.png",
        blank=True,
        null=True,
    )
    pais = models.CharField(max_length=50, blank=True, null= True)
    fecha_de_nacimiento = models.DateField (blank=True, null=True)
    direccion= models.CharField(max_length=100, blank=True, null=True)
    
    es_tasador = models.BooleanField(default=False)
    es_agente = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=False)

    activo = models.BooleanField(default=True)
    

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        roles = []
        if self.es_agente:
            roles.append("Agente")
        if self.es_tasador:
            roles.append("Tasador")
        if self.es_cliente:
            roles.append("Cliente")
        rol_str = ", ".join(roles) if roles else "Sin rol"
        return f"{self.username}: {self.last_name} {self.first_name} ({rol_str})"

