from rest_framework import serializers
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Producto.
    
    Proporciona validaciones automáticas y personalizada para los campos del producto.
    """
    
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'disponible',
            'fecha_creacion',
            'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_precio(self, value):
        """Validar que el precio sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        return value
    
    def validate_nombre(self, value):
        """Validar el nombre del producto"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es requerido.")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        
        return value.strip()
