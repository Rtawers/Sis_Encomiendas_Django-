# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importamos nuestras vistas personalizadas de autenticación
from envios import views_auth # ¡Aquí la importación!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('envios.urls')),

    # --- INICIO DE LA CORRECCIÓN: URLs de autenticación personalizadas ---
    path('accounts/login/', views_auth.login_view, name='login'),
    path('accounts/logout/', views_auth.logout_view, name='logout'),
    path('accounts/profile/', views_auth.perfil_view, name='profile'), # Añadimos perfil de una vez
    # --- FIN DE LA CORRECCIÓN ---
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)