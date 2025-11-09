from django.db import models
from usuarios.models import Usuario

class Tasacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('finalizada', 'Finalizada'),
    ]

    cliente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasaciones_como_cliente')
    agente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasaciones_como_agente')
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    localidad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    tipo_propiedad = models.CharField(max_length=50)
    superficie_total = models.FloatField(blank=True, null=True)
    superficie_cubierta = models.FloatField(blank=True, null=True)
    ambientes = models.IntegerField(blank=True, null=True)
    observaciones = models.TextField(blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Tasación #{self.id} - {self.nombre} ({self.localidad})"


class ImagenTasacion(models.Model):
    tasacion = models.ForeignKey(Tasacion, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='tasaciones/imagenes/')
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Imagen de Tasación #{self.tasacion.id}"