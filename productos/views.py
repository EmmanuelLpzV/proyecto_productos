from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Producto
from .serializers import (
    ProductoSerializer,
    ProductoCreateSerializer,
    ProductoListSerializer
)


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
    
    def get_serializer_class(self):
        """
        Retorna la clase de serializador apropiada según la acción.
        """
        if self.action == 'create':
            return ProductoCreateSerializer
        elif self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer
    
    @swagger_auto_schema(
        operation_description="Obtener lista de productos con filtros opcionales",
        manual_parameters=[
            openapi.Parameter(
                'disponible',
                openapi.IN_QUERY,
                description="Filtrar por disponibilidad (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Buscar en nombre y descripción",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Ordenar por campo (nombre, precio, fecha_creacion). Usar '-' para orden descendente",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Listar productos con filtros y búsqueda"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo producto",
        request_body=ProductoCreateSerializer,
        responses={
            201: ProductoSerializer,
            400: "Error de validación"
        }
    )
    def create(self, request, *args, **kwargs):
        """Crear un nuevo producto"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtener detalles de un producto específico",
        responses={
            200: ProductoSerializer,
            404: "Producto no encontrado"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """Obtener un producto específico"""
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar completamente un producto",
        request_body=ProductoSerializer,
        responses={
            200: ProductoSerializer,
            400: "Error de validación",
            404: "Producto no encontrado"
        }
    )
    def update(self, request, *args, **kwargs):
        """Actualizar completamente un producto"""
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un producto",
        request_body=ProductoSerializer,
        responses={
            200: ProductoSerializer,
            400: "Error de validación",
            404: "Producto no encontrado"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente un producto"""
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Eliminar un producto",
        responses={
            204: "Producto eliminado exitosamente",
            404: "Producto no encontrado"
        }
    )
    def destroy(self, request, *args, **kwargs):
        """Eliminar un producto"""
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_description="Obtener estadísticas de productos",
        responses={200: openapi.Response(
            description="Estadísticas de productos",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_productos': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'productos_disponibles': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'productos_no_disponibles': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'precio_promedio': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'precio_minimo': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'precio_maximo': openapi.Schema(type=openapi.TYPE_NUMBER),
                }
            )
        )}
    )
    def estadisticas(self, request):
        """Endpoint personalizado para obtener estadísticas de productos"""
        from django.db.models import Avg, Min, Max, Count
        
        queryset = self.get_queryset()
        stats = queryset.aggregate(
            total_productos=Count('id'),
            productos_disponibles=Count('id', filter=queryset.filter(disponible=True).query),
            precio_promedio=Avg('precio'),
            precio_minimo=Min('precio'),
            precio_maximo=Max('precio')
        )
        
        stats['productos_no_disponibles'] = stats['total_productos'] - stats['productos_disponibles']
        
        # Formatear precios
        for key in ['precio_promedio', 'precio_minimo', 'precio_maximo']:
            if stats[key] is not None:
                stats[key] = round(float(stats[key]), 2)
        
        return Response(stats)
