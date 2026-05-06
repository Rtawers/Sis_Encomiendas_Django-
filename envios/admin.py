# envios/admin.py
from django.contrib import admin
from django.utils.html import format_html

# Modelos de esta app
from .models import Empleado, Encomienda, HistorialEstado

# Models externos SOLO para uso (NO registrar)
from clientes.models import Cliente
from rutas.models import Ruta

from config.choices import EstadoEnvio, EstadoGeneral


# =============================================================================
# PERSONALIZACIÓN DEL TÍTULO DEL ADMIN
# =============================================================================
admin.site.site_header = '🚚 Sistema de Gestión de Encomiendas'
admin.site.site_title = 'Admin Encomiendas'
admin.site.index_title = 'Panel de Administración'


# =============================================================================
# COLORES PARA BADGES (estilos inline para que funcionen en el admin)
# =============================================================================
COLORES_ESTADO_ENVIO = {
    EstadoEnvio.PENDIENTE: '#6c757d',     # gris
    EstadoEnvio.EN_TRANSITO: '#0d6efd',   # azul
    EstadoEnvio.EN_DESTINO: '#ffc107',    # amarillo
    EstadoEnvio.ENTREGADO: '#198754',     # verde
    EstadoEnvio.DEVUELTO: '#dc3545',      # rojo
}

COLORES_ESTADO_GENERAL = {
    EstadoGeneral.ACTIVO: '#198754',      # verde
    EstadoGeneral.DE_BAJA: '#dc3545',     # rojo
}


def render_badge(color, texto):
    """Helper para renderizar badges con color de fondo en el admin."""
    return format_html(
        '<span style="background:{};color:white;padding:4px 10px;'
        'border-radius:5px;font-weight:bold;font-size:12px;">{}</span>',
        color,
        texto
    )


# -----------------------------------------------------------------------------
# ADMIN: ENCOMIENDA
# -----------------------------------------------------------------------------
@admin.register(Encomienda)
class EncomiendaAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'remitente_nombre',
        'destinatario_nombre',
        'ruta',
        'estado_badge',
        'peso_kg',
        'fecha_registro',
        'esta_entregada',
        'tiene_retraso',
    )

    list_filter = (
        'estado',
        'ruta',
        'fecha_registro',
        'fecha_entrega_est',
        'empleado_registro',
    )

    search_fields = (
        'codigo',
        'descripcion',
        'remitente__nombres',
        'remitente__apellidos',
        'destinatario__nombres',
        'destinatario__apellidos',
        'ruta__origen',
        'ruta__destino',
    )

    readonly_fields = (
        'codigo',
        'fecha_registro',
        'costo_envio',
    )

    ordering = ('-fecha_registro',)
    list_per_page = 20

    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'descripcion', 'peso_kg', 'volumen_cm3', 'costo_envio'),
        }),
        ('Partes', {
            'fields': ('remitente', 'destinatario', 'ruta', 'empleado_registro'),
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_entrega_est', 'fecha_entrega_real'),
            'classes': ('collapse',),
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',),
        }),
    )

    # -------------------------
    # MÉTODOS PERSONALIZADOS
    # -------------------------
    @admin.display(description='Remitente')
    def remitente_nombre(self, obj):
        return obj.remitente.nombre_completo

    @admin.display(description='Destinatario')
    def destinatario_nombre(self, obj):
        return obj.destinatario.nombre_completo

    @admin.display(description='Estado')
    def estado_badge(self, obj):
        color = COLORES_ESTADO_ENVIO.get(obj.estado, '#6c757d')
        return render_badge(color, obj.get_estado_display())

    # -------------------------
    # FILTRAR FOREIGN KEYS A SOLO ACTIVOS
    # -------------------------
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["remitente", "destinatario"]:
            kwargs["queryset"] = Cliente.objects.filter(estado=EstadoGeneral.ACTIVO)

        if db_field.name == "ruta":
            kwargs["queryset"] = Ruta.objects.filter(estado=EstadoGeneral.ACTIVO)

        if db_field.name == "empleado_registro":
            kwargs["queryset"] = Empleado.objects.filter(estado=EstadoGeneral.ACTIVO)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# -----------------------------------------------------------------------------
# ADMIN: EMPLEADO
# -----------------------------------------------------------------------------
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'user',
        'apellidos',
        'nombres',
        'cargo',
        'email',
        'telefono',
        'estado_badge',
        'fecha_ingreso',
    )

    list_filter = ('estado', 'cargo')
    search_fields = ('codigo', 'nombres', 'apellidos', 'email')
    ordering = ('-fecha_ingreso',)

    fieldsets = (
        ('Cuenta de usuario', {
            'fields': ('user',),
            'description': 'Asocia este empleado con un usuario del sistema para que pueda iniciar sesión.'
        }),
        ('Información personal', {
            'fields': ('codigo', 'nombres', 'apellidos')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Información laboral', {
            'fields': ('cargo', 'fecha_ingreso', 'estado')
        }),
    )

    @admin.display(description='Estado')
    def estado_badge(self, obj):
        color = COLORES_ESTADO_GENERAL.get(obj.estado, '#6c757d')
        return render_badge(color, obj.get_estado_display())


# -----------------------------------------------------------------------------
# ADMIN: HISTORIAL
# -----------------------------------------------------------------------------
@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):

    list_display = (
        'encomienda_link',
        'estado_anterior_badge',
        'estado_nuevo_badge',
        'empleado_nombre',
        'fecha_cambio',
    )

    list_filter = ('estado_nuevo', 'fecha_cambio')
    search_fields = ('encomienda__codigo', 'empleado__codigo')
    readonly_fields = ('fecha_cambio',)
    ordering = ('-fecha_cambio',)

    @admin.display(description='Encomienda')
    def encomienda_link(self, obj):
        from django.urls import reverse
        url = reverse("admin:envios_encomienda_change", args=[obj.encomienda.id])
        return format_html('<a href="{}">{}</a>', url, obj.encomienda.codigo)

    @admin.display(description='Empleado')
    def empleado_nombre(self, obj):
        return f'{obj.empleado.nombres} {obj.empleado.apellidos}'

    @admin.display(description='Antes')
    def estado_anterior_badge(self, obj):
        color = COLORES_ESTADO_ENVIO.get(obj.estado_anterior, '#6c757d')
        return render_badge(color, obj.get_estado_anterior_display())

    @admin.display(description='Después')
    def estado_nuevo_badge(self, obj):
        color = COLORES_ESTADO_ENVIO.get(obj.estado_nuevo, '#6c757d')
        return render_badge(color, obj.get_estado_nuevo_display())