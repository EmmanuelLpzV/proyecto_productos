from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models

from .models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar todas las operaciones CRUD de productos.
    
    Proporciona endpoints para:
    - GET /api/productos/ → Listar productos
    - POST /api/productos/ → Crear producto
    - GET /api/productos/{id}/ → Obtener producto específico
    - PUT /api/productos/{id}/ → Actualizar producto completo
    - PATCH /api/productos/{id}/ → Actualizar producto parcial
    - DELETE /api/productos/{id}/ → Eliminar producto
    """
    
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['disponible']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'precio', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint para obtener estadísticas de productos"""
        total_productos = Producto.objects.count()
        productos_disponibles = Producto.objects.filter(disponible=True).count()
        productos_no_disponibles = total_productos - productos_disponibles
        
        if total_productos > 0:
            precio_promedio = Producto.objects.aggregate(
                promedio=models.Avg('precio')
            )['promedio']
        else:
            precio_promedio = 0
            
        return Response({
            'total_productos': total_productos,
            'productos_disponibles': productos_disponibles,
            'productos_no_disponibles': productos_no_disponibles,
            'precio_promedio': round(float(precio_promedio or 0), 2)
        })
