from .models import Encomienda

def estadisticas_globales(request):
    if not request.user.is_authenticated:
        return {}

    nav_activas = Encomienda.objects.activas().count()
    nav_retraso = Encomienda.objects.con_retraso().count()
    nav_pendientes = Encomienda.objects.pendientes().count()

    return {
        'nav_activas': nav_activas,
        'nav_retraso': nav_retraso,
        'nav_pendientes': nav_pendientes,
    }