from django.apps import AppConfig

class RutasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rutas'

    def ready(self):
        from django.contrib import admin
        from django.conf import settings

        admin.site.site_header = settings.ADMIN_SITE_HEADER
        admin.site.site_title = settings.ADMIN_SITE_TITLE
        admin.site.index_title = settings.ADMIN_INDEX_TITLE