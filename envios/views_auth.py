# envios/views_auth.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticación de Django

# Decorador para vistas protegidas (aunque login_view no lo necesita)
from django.contrib.auth.decorators import login_required

def login_view(request):
    """
    Vista personalizada para el login de empleados.
    """
    # Si el usuario ya está autenticado, lo redirigimos al dashboard.
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirige al nombre de URL 'dashboard'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password) # Intenta autenticar

            if user is not None:
                login(request, user) # Inicia sesión
                messages.success(request, f'¡Bienvenido, {user.get_full_name() or user.username}!')

                # Redirigir a la página solicitada originalmente o al dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = AuthenticationForm() # Formulario vacío para GET

    # Pasamos el formulario y el valor 'next' al contexto del template
    context = {'form': form, 'next': request.GET.get('next', '')}
    return render(request, 'accounts/login.html', context) # Renderizamos nuestra plantilla

@login_required # Protegemos esta vista para que solo usuarios logueados puedan hacer logout
def logout_view(request):
    """
    Cierra la sesión del usuario.
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login') # Redirige a nuestra vista de login después del logout

@login_required
def perfil_view(request):
    """
    Vista de perfil del empleado autenticado.
    """
    context = {'user': request.user}
    return render(request, 'accounts/perfil.html', context)