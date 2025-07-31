# 📦 Gestión de Productos - API REST con Django

Microservicio desarrollado con Django REST Framework para la gestión completa de productos mediante una API RESTful. El sistema permite crear, leer, actualizar y eliminar productos, y está completamente dockerizado para facilitar el despliegue.

## 🚀 Características

- ✅ API REST completa para gestión de productos (CRUD)
- ✅ Django 4.2+ y Django REST Framework
- ✅ Base de datos SQLite
- ✅ Documentación automática con Swagger y ReDoc
- ✅ Filtros, búsqueda y ordenamiento
- ✅ Validaciones personalizadas
- ✅ Pruebas unitarias y de integración
- ✅ Dockerización completa
- ✅ Panel de administración Django

## 📋 Modelo de Datos

El modelo `Producto` incluye los siguientes campos:

```python
- id: Identificador único (auto generado)
- nombre: Nombre del producto (CharField, requerido)
- descripcion: Descripción del producto (TextField, opcional)
- precio: Precio del producto (DecimalField, requerido)
- disponible: Disponibilidad del producto (BooleanField, default=True)
- fecha_creacion: Fecha de creación (DateTimeField, auto)
- fecha_actualizacion: Fecha de actualización (DateTimeField, auto)
```

## 🔗 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/productos/` | Listar todos los productos |
| `POST` | `/api/productos/` | Crear un nuevo producto |
| `GET` | `/api/productos/{id}/` | Obtener un producto específico |
| `PUT` | `/api/productos/{id}/` | Actualizar completamente un producto |
| `PATCH` | `/api/productos/{id}/` | Actualizar parcialmente un producto |
| `DELETE` | `/api/productos/{id}/` | Eliminar un producto |
| `GET` | `/api/productos/estadisticas/` | Obtener estadísticas de productos |

### Parámetros de consulta disponibles:

- `?disponible=true/false` - Filtrar por disponibilidad
- `?search=texto` - Buscar en nombre y descripción
- `?ordering=campo` - Ordenar por campo (nombre, precio, fecha_creacion)
- `?ordering=-campo` - Ordenar descendente (agregar `-`)

## 🛠️ Instalación y Configuración

### Opción 1: Instalación Local

#### Requisitos previos
- Python 3.8+
- pip

#### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd proyecto_productos
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv

# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

6. **Iniciar el servidor de desarrollo**
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000`

### Opción 2: Instalación con Docker (Recomendada)

#### Requisitos previos
- Docker
- Docker Compose

#### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd proyecto_productos
```

2. **Construir y levantar los contenedores**
```bash
docker-compose up --build
```

3. **En otra terminal, ejecutar migraciones**
```bash
docker-compose exec web python manage.py migrate
```

4. **Crear superusuario (opcional)**
```bash
docker-compose exec web python manage.py createsuperuser
```

La API estará disponible en: `http://localhost:8000`

Para detener los contenedores:
```bash
docker-compose down
```

## 📖 Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a la documentación interactiva:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **JSON Schema**: `http://localhost:8000/swagger.json`
- **Panel de Admin**: `http://localhost:8000/admin/`

## 🧪 Ejecutar Pruebas

### Instalación local
```bash
# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas específicas
python manage.py test productos.tests

# Ejecutar con coverage (instalar coverage primero)
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML
```

### Con Docker
```bash
# Ejecutar todas las pruebas
docker-compose exec web python manage.py test

# Ejecutar pruebas específicas
docker-compose exec web python manage.py test productos.tests
```

## 📝 Ejemplos de Uso

### Crear un producto
```bash
curl -X POST http://localhost:8000/api/productos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "iPhone 15",
    "descripcion": "Smartphone Apple última generación",
    "precio": "25999.99",
    "disponible": true
  }'
```

### Listar productos
```bash
curl http://localhost:8000/api/productos/
```

### Buscar productos
```bash
curl "http://localhost:8000/api/productos/?search=iPhone"
```

### Filtrar productos disponibles
```bash
curl "http://localhost:8000/api/productos/?disponible=true"
```

### Obtener estadísticas
```bash
curl http://localhost:8000/api/productos/estadisticas/
```

### Actualizar un producto
```bash
curl -X PUT http://localhost:8000/api/productos/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "iPhone 15 Pro",
    "descripcion": "Smartphone Apple Pro última generación",
    "precio": "29999.99",
    "disponible": true
  }'
```

### Eliminar un producto
```bash
curl -X DELETE http://localhost:8000/api/productos/1/
```

### Variables de Entorno

Puedes personalizar la configuración usando variables de entorno:

- `DEBUG`: Modo debug (default: True)
- `SECRET_KEY`: Clave secreta de Django
- `ALLOWED_HOSTS`: Hosts permitidos

### Base de Datos

Por defecto usa SQLite, pero puedes cambiar a PostgreSQL modificando `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'productos_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔧 Comandos Útiles

### Django Management
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Colectar archivos estáticos
python manage.py collectstatic

# Shell interactivo
python manage.py shell
```

### Docker
```bash
# Ver logs
docker-compose logs

# Ejecutar comandos en el contenedor
docker-compose exec web python manage.py <comando>

# Reconstruir contenedores
docker-compose up --build

# Limpiar contenedores e imágenes
docker-compose down
docker system prune
```

## 🐛 Solución de Problemas

### Error de migraciones
```bash
# Resetear migraciones (CUIDADO: borra datos)
python manage.py migrate productos zero
python manage.py migrate
```

### Puerto ocupado
Si el puerto 8000 está ocupado, cambia el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Cambia el primer número
```

### Problemas de permisos en Docker
```bash
# En Linux/macOS, asegurar permisos
sudo chown -R $USER:$USER .
```

## 📋 TODO / Mejoras Futuras

- [ ] Autenticación y autorización (JWT)
- [ ] Paginación avanzada
- [ ] Caché con Redis
- [ ] Subida de imágenes de productos
- [ ] Categorías de productos
- [ ] Webhooks para notificaciones
- [ ] Métricas y monitoreo
- [ ] CI/CD con GitHub Actions

