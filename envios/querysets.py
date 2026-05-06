# envios/querysets.py

from django.db import models
from django.db.models import Q
from django.utils import timezone

from config.choices import EstadoEnvio, EstadoGeneral


# =========================
# ENCOMIENDAS
# =========================
class EncomiendaQuerySet(models.QuerySet):

    def con_relaciones(self):
        return self.select_related(
            'remitente',
            'destinatario',
            'ruta',
            'empleado_registro'
        )

    def activas(self):
        return self.exclude(
            estado__in=[EstadoEnvio.ENTREGADO, EstadoEnvio.DEVUELTO]
        )

    def pendientes(self):
        return self.filter(estado=EstadoEnvio.PENDIENTE)

    def en_transito(self):
        return self.filter(estado=EstadoEnvio.EN_TRANSITO)

    def entregadas(self):
        return self.filter(estado=EstadoEnvio.ENTREGADO)

    def devueltas(self):
        return self.filter(estado=EstadoEnvio.DEVUELTO)

    def con_retraso(self):
        return self.activas().filter(
            fecha_entrega_est__lt=timezone.now().date()
        )

    def por_ruta(self, ruta_obj):
        return self.filter(ruta=ruta_obj)

    def por_remitente(self, cliente_obj):
        return self.filter(remitente=cliente_obj)

    def por_destinatario(self, cliente_obj):
        return self.filter(destinatario=cliente_obj)

    def en_transito_por_ruta(self, ruta_obj):
        return self.en_transito().por_ruta(ruta_obj)


# =========================
# CLIENTES
# =========================
class ClienteQuerySet(models.QuerySet):

    def activos(self):
        return self.filter(estado=EstadoGeneral.ACTIVO)

    def de_baja(self):
        return self.filter(estado=EstadoGeneral.DE_BAJA)

    def buscar(self, termino):
        if not termino:
            return self

        return self.filter(
            Q(nombres__icontains=termino) |
            Q(apellidos__icontains=termino) |
            Q(nro_doc__icontains=termino)
        )


# =========================
# RUTAS
# =========================
class RutaQuerySet(models.QuerySet):

    def activos(self):
        return self.filter(estado=EstadoGeneral.ACTIVO)

    def de_baja(self):
        return self.filter(estado=EstadoGeneral.DE_BAJA)

    def por_origen(self, ciudad):
        return self.filter(origen__icontains=ciudad)

    def por_destino(self, ciudad):
        return self.filter(destino__icontains=ciudad)