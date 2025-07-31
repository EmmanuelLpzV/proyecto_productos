# Script de configuración inicial para el proyecto de gestión de productos
echo "🚀 Configurando proyecto de Gestión de Productos..."

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependencias
echo "Verificando dependencias..."

if ! command_exists python3; then
    echo "Python 3 no está instalado. Por favor instala Python 3.8+"
    exit 1
fi

if ! command_exists pip; then
    echo "pip no está instalado. Por favor instala pip"
    exit 1
fi

echo "Python y pip están disponibles"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
else
    echo "Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Crear datos de prueba
echo "Creando datos de prueba..."
python manage.py shell << EOF
from productos.models import Producto
from decimal import Decimal

# Verificar si ya existen productos
if not Producto.objects.exists():
    productos_demo = [
        {
            'nombre': 'iPhone 15 Pro',
            'descripcion': 'Smartphone Apple con chip A17 Pro, pantalla de 6.1 pulgadas y cámara de 48MP',
            'precio': Decimal('25999.99'),
            'disponible': True
        },
        {
            'nombre': 'Samsung Galaxy S24',
            'descripcion': 'Smartphone Android con pantalla AMOLED de 6.2 pulgadas y cámara de 50MP',
            'precio': Decimal('22999.99'),
            'disponible': True
        },
        {
            'nombre': 'MacBook Air M3',
            'descripcion': 'Laptop Apple con chip M3, 8GB RAM y 256GB SSD',
            'precio': Decimal('32999.99'),
            'disponible': False
        },
        {
            'nombre': 'AirPods Pro 2',
            'descripcion': 'Audífonos inalámbricos con cancelación de ruido activa',
            'precio': Decimal('6999.99'),
            'disponible': True
        },
        {
            'nombre': 'PlayStation 5',
            'descripcion': 'Consola de videojuegos de última generación con SSD ultra rápido',
            'precio': Decimal('13999.99'),
            'disponible': False
        }
    ]
    
    for producto_data in productos_demo:
        Producto.objects.create(**producto_data)
    
    print(f"Se crearon {len(productos_demo)} productos de demostración")
else:
    print("Ya existen productos en la base de datos")
EOF

# Colectar archivos estáticos
echo "Colectando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar pruebas
echo "Ejecutando pruebas..."
python manage.py test productos.tests

echo ""
echo "¡Configuración completada exitosamente!"
echo ""
echo "Próximos pasos:"
echo "1. Activar el entorno virtual: source venv/bin/activate"
echo "2. Iniciar el servidor: python manage.py runserver"
echo "3. Visitar: http://localhost:8000/api/productos/"
echo "4. Documentación: http://localhost:8000/swagger/"
echo ""
echo "Comandos útiles:"
echo "- Crear superusuario: python manage.py createsuperuser"
echo "- Ejecutar pruebas: python manage.py test"
echo "- Acceder al shell: python manage.py shell"
echo ""

# Verificar si Docker está disponible
if command_exists docker && command_exists docker-compose; then
    echo "Docker está disponible. También puedes usar:"
    echo "- docker-compose up --build"
    echo ""
fi

echo "¡El proyecto está listo para usar!"
