from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, RegisterSellerForm, LoginForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importar correctamente desde django.contrib

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro completado con éxito. Por favor, inicia sesión.")
            return redirect('login')  # Redirigir al login después del registro exitoso
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def registro_vendedor(request):
    if request.method == 'POST':
        seller_form = RegisterSellerForm(request.POST)
        if seller_form.is_valid():
            seller_form.save()
            messages.success(request, "Registro de vendedor completado con éxito. Por favor, inicia sesión.")
            return redirect('login')  # Redirigir al login después del registro exitoso
    else:
        seller_form = RegisterSellerForm()

    return render(request, 'users/register.html', {'form': RegisterForm(), 'seller_form': seller_form})

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
