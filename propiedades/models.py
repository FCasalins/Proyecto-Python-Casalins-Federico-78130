from django.db import models
from usuarios.models import Usuario


class Propiedad(models.Model):
    OPERACION_CHOICES = [
        ('venta', 'Venta'),
        ('alquiler', 'Alquiler'),
        ('alquiler_temporario', 'Alquiler Temporario'),
    ]
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('lote', 'Lote'),
        ('local', 'Local Comercial'),
        ('campo', 'Campo'),
        ('quinta', 'Quinta'),
        ('ph', 'PH'),
    ]
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('reservada', 'Reservada'),
        ('vendida', 'Vendida / Alquilada'),
    ]

    codigo = models.IntegerField(unique=True)
    operacion = models.CharField(max_length=30, choices=OPERACION_CHOICES)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    orientacion = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=50, blank=True, null=True)
    calle = models.CharField(max_length=100)
    superficie_total = models.FloatField()
    superficie_cubierta = models.FloatField(blank=True, null=True)
    ambientes = models.IntegerField()
    dormitorios = models.IntegerField(blank=True, null=True)
    banios = models.IntegerField(blank=True, null=True)
    cochera = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=10, default='USD')
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='disponible')
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    imagen_principal = models.ImageField(upload_to='propiedades/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'

    def __str__(self):
        return f"{self.tipo.capitalize()} en {self.localidad} - {self.operacion.capitalize()} (${self.precio:,.0f})"


Propiedad.add_to_class(
    'agente',
    models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        related_name='propiedades',
        null=True,
        blank=True,
    )
)

class ImagenPropiedad(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='propiedades/')
    descripcion = models.CharField(max_length=200, blank=True)
    destacada = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Imagen de Propiedad'
        verbose_name_plural = 'Imágenes de Propiedades'
    def __str__(self):
        return f"Imagen de {self.propiedad}"


class Consulta(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='consultas')
    cliente = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, blank=True, null=True, related_name='consultas')
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Consulta de {self.nombre} por {self.propiedad}"