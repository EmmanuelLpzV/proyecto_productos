from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    
    list_display = [
        'id',
        'nombre',
        'precio',
        'disponible',
        'fecha_creacion',
        'fecha_actualizacion'
    ]
    
    list_filter = [
        'disponible',
        'fecha_creacion',
        'fecha_actualizacion'
    ]
    
    search_fields = [
        'nombre',
        'descripcion'
    ]
    
    list_editable = [
        'disponible',
        'precio'
    ]
    
    readonly_fields = [
        'fecha_creacion',
        'fecha_actualizacion'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Información Comercial', {
            'fields': ('precio', 'disponible')
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-fecha_creacion']
    list_per_page = 25
    
    def get_queryset(self, request):
        return super().get_queryset(request)
