from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre del producto', max_length=200, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, help_text='Descripción detallada del producto', null=True, verbose_name='Descripción')),
                ('precio', models.DecimalField(decimal_places=2, help_text='Precio del producto en pesos mexicanos', max_digits=10, verbose_name='Precio')),
                ('disponible', models.BooleanField(default=True, help_text='Indica si el producto está disponible para venta', verbose_name='Disponible')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-fecha_creacion'],
                'indexes': [models.Index(fields=['nombre'], name='productos_p_nombre_456643_idx'), models.Index(fields=['disponible'], name='productos_p_disponi_9963a6_idx'), models.Index(fields=['precio'], name='productos_p_precio_d043df_idx')],
            },
        ),
    ]
