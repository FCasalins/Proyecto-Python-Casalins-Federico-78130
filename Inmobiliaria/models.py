from django.db import models

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

class Agente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='agentes/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    es_tasador = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Agente'
        verbose_name_plural = 'Agentes'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        rol = " (Tasador)" if self.es_tasador else ""
        return f"{self.nombre} {self.apellido}{rol}"

Propiedad.add_to_class(
    'agente',
    models.ForeignKey(
        Agente,
        on_delete=models.SET_NULL,
        related_name='propiedades',
        null=True,
        blank=True,
    )
)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.IntegerField(unique=True)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    localidad = models.CharField(max_length=100)

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"Nombre: {self.nombre}, {self.apellido}" 
    
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
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True, related_name='consultas')
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Consulta de {self.nombre} por {self.propiedad}"
    
class Tasacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('finalizada', 'Finalizada'),
    ]

    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasaciones')
    agente = models.ForeignKey('Agente', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasaciones')
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