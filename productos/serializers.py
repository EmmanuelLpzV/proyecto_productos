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
    
    def to_representation(self, instance):
        """Personalizar la representación del objeto"""
        data = super().to_representation(instance)
        
        # Formatear el precio para mostrar con símbolo de peso
        if data.get('precio'):
            data['precio_formateado'] = f"${data['precio']} MXN"
        
        return data


class ProductoCreateSerializer(ProductoSerializer):
    """
    Serializador específico para la creación de productos.
    Excluye campos que no son necesarios en la creación.
    """
    
    class Meta(ProductoSerializer.Meta):
        fields = ['nombre', 'descripcion', 'precio', 'disponible']


class ProductoListSerializer(serializers.ModelSerializer):
    """
    Serializador ligero para listar productos.
    Solo incluye los campos esenciales para mejorar performance.
    """
    precio_formateado = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'precio_formateado', 'disponible']
    
    def get_precio_formateado(self, obj):
        """Formatear el precio con símbolo de peso"""
        return f"${obj.precio} MXN"
