from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .models import Producto


class ProductoModelTest(TestCase):
    """Pruebas unitarias para el modelo Producto"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.producto_data = {
            'nombre': 'Producto de Prueba',
            'descripcion': 'Descripción del producto de prueba',
            'precio': Decimal('99.99'),
            'disponible': True
        }
    
    def test_crear_producto(self):
        """Probar la creación de un producto"""
        producto = Producto.objects.create(**self.producto_data)
        
        self.assertEqual(producto.nombre, 'Producto de Prueba')
        self.assertEqual(producto.precio, Decimal('99.99'))
        self.assertTrue(producto.disponible)
        self.assertIsNotNone(producto.fecha_creacion)
        self.assertIsNotNone(producto.fecha_actualizacion)
    
    def test_str_representation(self):
        """Probar la representación string del producto"""
        producto = Producto.objects.create(**self.producto_data)
        expected_str = f"{producto.nombre} - ${producto.precio}"
        self.assertEqual(str(producto), expected_str)
    
    def test_validacion_precio_negativo(self):
        """Probar que no se puede crear un producto con precio negativo"""
        from django.core.exceptions import ValidationError
        
        self.producto_data['precio'] = Decimal('-10.00')
        producto = Producto(**self.producto_data)
        
        with self.assertRaises(ValidationError):
            producto.clean()
    
    def test_validacion_nombre_vacio(self):
        """Probar que no se puede crear un producto con nombre vacío"""
        from django.core.exceptions import ValidationError
        
        self.producto_data['nombre'] = ''
        producto = Producto(**self.producto_data)
        
        with self.assertRaises(ValidationError):
            producto.clean()
    
    def test_disponible_default_true(self):
        """Probar que el campo disponible tiene valor por defecto True"""
        del self.producto_data['disponible']
        producto = Producto.objects.create(**self.producto_data)
        self.assertTrue(producto.disponible)


class ProductoAPITest(APITestCase):
    """Pruebas de integración para la API de productos"""
    
    def setUp(self):
        """Configuración inicial para las pruebas de API"""
        self.client = APIClient()
        self.producto_data = {
            'nombre': 'Producto API Test',
            'descripcion': 'Descripción del producto API',
            'precio': '149.99',
            'disponible': True
        }
        
        # Crear un producto de prueba
        self.producto = Producto.objects.create(
            nombre='Producto Existente',
            descripcion='Descripción existente',
            precio=Decimal('199.99'),
            disponible=True
        )
    
    def test_listar_productos(self):
        """Probar GET /api/productos/"""
        url = reverse('producto-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Producto Existente')
    
    def test_crear_producto(self):
        """Probar POST /api/productos/"""
        url = reverse('producto-list')
        response = self.client.post(url, self.producto_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Producto API Test')
    
    def test_obtener_producto_detalle(self):
        """Probar GET /api/productos/{id}/"""
        url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Producto Existente')
        self.assertEqual(str(response.data['precio']), '199.99')
    
    def test_actualizar_producto(self):
        """Probar PUT /api/productos/{id}/"""
        url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        updated_data = {
            'nombre': 'Producto Actualizado',
            'descripcion': 'Nueva descripción',
            'precio': '299.99',
            'disponible': False
        }
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Producto Actualizado')
        self.assertEqual(str(self.producto.precio), '299.99')
        self.assertFalse(self.producto.disponible)
    
    def test_actualizar_parcial_producto(self):
        """Probar PATCH /api/productos/{id}/"""
        url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        partial_data = {'precio': '249.99'}
        response = self.client.patch(url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(str(self.producto.precio), '249.99')
        self.assertEqual(self.producto.nombre, 'Producto Existente')  # No cambió
    
    def test_eliminar_producto(self):
        """Probar DELETE /api/productos/{id}/"""
        url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Producto.objects.count(), 0)
    
    def test_crear_producto_precio_invalido(self):
        """Probar creación con precio inválido"""
        url = reverse('producto-list')
        invalid_data = self.producto_data.copy()
        invalid_data['precio'] = '-10.00'
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('precio', response.data)
    
    def test_crear_producto_nombre_vacio(self):
        """Probar creación con nombre vacío"""
        url = reverse('producto-list')
        invalid_data = self.producto_data.copy()
        invalid_data['nombre'] = ''
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre', response.data)
    
    def test_filtrar_productos_por_disponibilidad(self):
        """Probar filtro por disponibilidad"""
        # Crear producto no disponible
        Producto.objects.create(
            nombre='Producto No Disponible',
            precio=Decimal('99.99'),
            disponible=False
        )
        
        url = reverse('producto-list')
        response = self.client.get(url, {'disponible': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue(response.data['results'][0]['disponible'])
    
    def test_buscar_productos(self):
        """Probar búsqueda de productos"""
        url = reverse('producto-list')
        response = self.client.get(url, {'search': 'Existente'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Existente', response.data['results'][0]['nombre'])
    
    def test_estadisticas_productos(self):
        """Probar endpoint de estadísticas"""
        url = reverse('producto-estadisticas')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_productos', response.data)
        self.assertIn('productos_disponibles', response.data)
        self.assertIn('precio_promedio', response.data)
        self.assertEqual(response.data['total_productos'], 1)
    
    def test_obtener_producto_inexistente(self):
        """Probar obtener producto que no existe"""
        url = reverse('producto-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
