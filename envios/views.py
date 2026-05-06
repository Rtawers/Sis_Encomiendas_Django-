# envios/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages  #  mensajes flash
from django.views.decorators.http import require_POST # Para asegurar que ciertas vistas solo acepten POST
from django.core.exceptions import ValidationError as DjangoValidationError # Renombramos para evitar conflicto con nuestro ValidationError


# Modelos
from .models import Encomienda, Empleado, HistorialEstado
from clientes.models import Cliente
from rutas.models import Ruta
from config.choices import EstadoEnvio, TipoDocumento

# Formulario
from .forms import EncomiendaForm


COLORES_ESTADO = {
    'primary': '#0d6efd',
    'info': '#0d6efd',
    'danger': '#dc3545',
    'success': '#198754',
}


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):
    hoy = timezone.now().date()

    total_activas = Encomienda.objects.activas().count()
    en_transito = Encomienda.objects.en_transito().count()
    con_retraso = Encomienda.objects.con_retraso().count()

    entregadas_hoy = Encomienda.objects.filter(
        estado=EstadoEnvio.ENTREGADO,
        fecha_entrega_real=hoy
    ).count()

    ultimas_encomiendas = (
        Encomienda.objects
        .con_relaciones()
        .order_by('-fecha_registro')[:5]
    )

    context = {
        'total_activas': total_activas,
        'en_transito': en_transito,
        'con_retraso': con_retraso,
        'entregadas_hoy': entregadas_hoy,
        'ultimas': ultimas_encomiendas,
        'stats_cards': [
            {'label': 'Activas', 'valor': total_activas, 'color': COLORES_ESTADO['primary'], 'icono': 'shipping-fast'},
            {'label': 'En tránsito', 'valor': en_transito, 'color': COLORES_ESTADO['info'], 'icono': 'truck'},
            {'label': 'Con retraso', 'valor': con_retraso, 'color': COLORES_ESTADO['danger'], 'icono': 'exclamation-triangle'},
            {'label': 'Entregadas hoy', 'valor': entregadas_hoy, 'color': COLORES_ESTADO['success'], 'icono': 'check-circle'},
        ]
    }

    return render(request, 'envios/dashboard.html', context)


# =========================
# LISTA DE ENCOMIENDAS
# =========================
@login_required
def encomienda_lista(request):

    qs = (
        Encomienda.objects
        .con_relaciones()
        .order_by('-fecha_registro')
    )

    # 🔍 Filtros
    estado_activo = request.GET.get('estado', '')
    query = request.GET.get('q', '')

    if estado_activo:
        qs = qs.filter(estado=estado_activo)

    if query:
        qs = qs.filter(
            Q(codigo__icontains=query) |
            Q(remitente__nombres__icontains=query) |
            Q(remitente__apellidos__icontains=query) |
            Q(destinatario__nombres__icontains=query) |
            Q(destinatario__apellidos__icontains=query)
        )

    #  Paginación
    paginator = Paginator(qs, 15)
    page_number = request.GET.get('page', 1)
    encomiendas = paginator.get_page(page_number)

    context = {
        'encomiendas': encomiendas,
        'estados': EstadoEnvio.choices,
        'estado_activo': estado_activo,
        'query': query,
    }

    return render(request, 'envios/lista.html', context)


# =========================
# DETALLE DE ENCOMIENDA
# =========================
@login_required
def encomienda_detalle(request, pk):

    encomienda = get_object_or_404(
        Encomienda.objects.con_relaciones(),
        pk=pk
    )

    historial = (
        encomienda.historial
        .select_related('empleado')
        .order_by('-fecha_cambio')
    )

    context = {
        'encomienda': encomienda,
        'historial': historial,
        'estados': EstadoEnvio.choices
    }

    return render(request, 'envios/detalle.html', context)


# =========================
# CREAR ENCOMIENDA (PRG)
# =========================
@login_required
def encomienda_crear(request):

    if request.method == 'POST':
        form = EncomiendaForm(request.POST)

        if form.is_valid():
            # 1. Verificar que el usuario tenga empleado asociado
            if not hasattr(request.user, 'empleado'):
                messages.error(
                    request,
                    'Error: Tu usuario no está asociado a un Empleado. Contacta al administrador.'
                )
                return render(
                    request,
                    'envios/form.html',
                    {'form': form, 'titulo': 'Nueva Encomienda'}
                )

            # 2. Crear la encomienda sin guardarla aún
            encomienda = form.save(commit=False)

            # 3. Asignar el empleado logueado
            encomienda.empleado_registro = request.user.empleado

            # 4. Guardar (el modelo genera código y costo automáticamente)
            try:
                encomienda.save()
                messages.success(
                    request,
                    f'¡Encomienda {encomienda.codigo} registrada correctamente!'
                )
                return redirect('encomienda_detalle', pk=encomienda.pk)

            except Exception as e:
                messages.error(
                    request,
                    f'Error al guardar la encomienda: {e}'
                )

        else:
            messages.error(
                request,
                'Por favor corrige los errores del formulario.'
            )

    else:
        form = EncomiendaForm()

    context = {
        'form': form,
        'titulo': 'Nueva Encomienda',
    }

    return render(request, 'envios/form.html', context)

# =========================
# CAMBIAR ESTADO 
# =========================

@login_required
@require_POST # <-- Buena práctica: esta vista solo acepta solicitudes POST

def encomienda_cambiar_estado(request, pk):
    """
    Vista para cambiar el estado de una encomienda específica.
    Solo acepta solicitudes POST.
    """
    encomienda = get_object_or_404(Encomienda, pk=pk)

    nuevo_estado = request.POST.get('estado')
    observacion = request.POST.get('observacion', '')

    # Buscamos el empleado que realiza el cambio (el usuario logueado)
    
    if not hasattr(request.user, 'empleado'):
        messages.error(request, 'Error: Tu usuario no está asociado a un Empleado. No se puede cambiar el estado.')
        return redirect('encomienda_detalle', pk=encomienda.pk)

    empleado_cambio = request.user.empleado

    try:
        # Usamos el método de negocio del modelo para cambiar el estado
        encomienda.cambiar_estado(nuevo_estado, empleado_cambio, observacion)
        messages.success(request, f'Estado de encomienda {encomienda.codigo} actualizado a {encomienda.get_estado_display()}.')
    except ValueError as e: # Capturamos el ValueError que puede lanzar el modelo (ej. estado igual)
        messages.error(request, f'No se pudo actualizar el estado: {e}')
    except DjangoValidationError as e: # Capturamos si el modelo lanza ValidationError
        messages.error(request, f'Error de validación al cambiar estado: {e}')
    except Exception as e: # Captura cualquier otra excepción inesperada
        messages.error(request, f'Ocurrió un error inesperado al cambiar el estado: {e}')

    return redirect('encomienda_detalle', pk=encomienda.pk) # Siempre redirigimos de vuelta al detalle