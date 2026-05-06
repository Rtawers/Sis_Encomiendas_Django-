# rutas/admin.py
from django.contrib import admin
from django.utils.html import format_html

from .models import Ruta
from config.choices import EstadoGeneral


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'origen',
        'destino',
        'precio_base',
        'dias_entrega',
        'estado_badge',
    )
    list_filter = ('estado', 'dias_entrega')
    search_fields = ('codigo', 'origen', 'destino', 'descripcion')
    ordering = ('origen', 'destino',)
    list_per_page = 20

    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'descripcion')
        }),
        ('Trayecto', {
            'fields': ('origen', 'destino', 'dias_entrega')
        }),
        ('Tarifa', {
            'fields': ('precio_base',)
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )

    @admin.display(description='Estado')
    def estado_badge(self, obj):
        colores = {
            EstadoGeneral.ACTIVO: '#198754',
            EstadoGeneral.DE_BAJA: '#dc3545',
        }
        color = colores.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;'
            'border-radius:5px;font-weight:bold;font-size:12px;">{}</span>',
            color,
            obj.get_estado_display()
        )