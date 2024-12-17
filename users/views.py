from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, RegisterSellerForm, LoginForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importar correctamente desde django.contrib

def register_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Identifica el formulario enviado

        # Procesar formulario de registro de usuario
        if form_type == 'user_register':
            user_form = RegisterForm(request.POST)
            seller_form = RegisterSellerForm()  # Formulario vacío
            if user_form.is_valid():
                user_form.save()
                messages.success(request, '¡Usuario registrado correctamente!')
                return redirect('login')
            else:
                messages.error(request, 'Error al registrar usuario. Verifique los datos.')

        # Procesar formulario de registro de vendedor
        elif form_type == 'seller_register':
            seller_form = RegisterSellerForm(request.POST)
            user_form = RegisterForm()  # Formulario vacío
            if seller_form.is_valid():
                seller_form.save()
                messages.success(request, '¡Vendedor registrado correctamente!')
                return redirect('login')
            else:
                messages.error(request, 'Error al registrar vendedor. Verifique los datos.')
    else:
        user_form = RegisterForm()
        seller_form = RegisterSellerForm()

    # Renderiza ambos formularios en el template
    return render(request, 'users/register.html', {
        'user_form': user_form,
        'seller_form': seller_form
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Iniciar sesión
            login(request, user)
            print(f"Usuario logeado: {user.username}, es vendedor: {user.is_seller}")  # Verifica el valor de is_seller
            # Verificar si el usuario es vendedor
            if user.is_seller:
                return redirect('listar_productos_vendedor')  # Redirigir al perfil de vendedor

            # Si no es vendedor, redirigir a la página principal
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')
