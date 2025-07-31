from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

# Crear el router y registrar el viewset
router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

# Las URLs generadas automáticamente por el router son:
# GET /api/productos/ → Listar productos
# POST /api/productos/ → Crear producto
# GET /api/productos/{id}/ → Obtener producto específico
# PUT /api/productos/{id}/ → Actualizar producto completo
# PATCH /api/productos/{id}/ → Actualizar producto parcial
# DELETE /api/productos/{id}/ → Eliminar producto
# GET /api/productos/estadisticas/ → Obtener estadísticas

urlpatterns = [
    path('', include(router.urls)),
]
