# clientes/admin.py
from django.contrib import admin
from django.utils.html import format_html

from .models import Cliente
from config.choices import EstadoGeneral


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nro_doc',
        'tipo_doc',
        'nombre_completo',
        'email',
        'telefono',
        'estado_badge',
        'fecha_registro',
    )
    list_filter = ('estado', 'tipo_doc')
    search_fields = ('nro_doc', 'nombres', 'apellidos', 'email')
    ordering = ('apellidos', 'nombres',)
    list_per_page = 20

    fieldsets = (
        ('Identificación', {
            'fields': ('tipo_doc', 'nro_doc')
        }),
        ('Información personal', {
            'fields': ('nombres', 'apellidos')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )

    @admin.display(description='Nombre Completo', ordering='apellidos')
    def nombre_completo(self, obj):
        return obj.nombre_completo

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