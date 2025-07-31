from django.db import models
from decimal import Decimal


class Producto(models.Model):
    """
    Modelo para representar un producto en el sistema.
    
    Campos:
    - id: Identificador único autogenerado
    - nombre: Nombre del producto (requerido)
    - descripcion: Descripción del producto (opcional)
    - precio: Precio del producto (requerido)
    - disponible: Indica si el producto está disponible (default: True)
    """
    
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre",
        help_text="Nombre del producto"
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del producto"
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio",
        help_text="Precio del producto en pesos mexicanos"
    )
    
    disponible = models.BooleanField(
        default=True,
        verbose_name="Disponible",
        help_text="Indica si el producto está disponible para venta"
    )
    
    # Timestamps automáticos
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['disponible']),
            models.Index(fields=['precio']),
        ]
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    def clean(self):
        """Validaciones personalizadas del modelo"""
        from django.core.exceptions import ValidationError
        
        if self.precio is not None and self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a cero.")
        
        if self.nombre:
            self.nombre = self.nombre.strip()
            if len(self.nombre) < 2:
                raise ValidationError("El nombre debe tener al menos 2 caracteres.")
    
    def save(self, *args, **kwargs):
        """Sobrescribir save para ejecutar validaciones"""
        self.clean()
        super().save(*args, **kwargs)
