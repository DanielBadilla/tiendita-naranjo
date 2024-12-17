# views.py (en la carpeta products)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import ProductForm
from orders.models import Order
from products.models import Product
from django.urls import reverse


class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de Productos'
        context['products'] = context['product_list']
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductSearchListView(ListView):
    template_name = 'products/search.html'

    def get_queryset(self):
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()
        return context

def login_required_with_message(view_func):
    """
    Decorador que combina @login_required con un mensaje personalizado.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Debes loguearte o registrarte para continuar.")
            return redirect(f"{reverse('login')}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_with_message
def agregar_producto(request):
    if not request.user.is_seller:
        messages.error(request, "No tienes permisos para agregar productos.")
        return redirect('index')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.stock = request.POST.get('stock', 0)  # Añadir el campo de stock
            producto.save()
            messages.success(request, "Producto agregado con éxito.")
            return redirect('listar_productos_vendedor')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required_with_message
def listar_productos_vendedor(request):
    if not request.user.is_seller:
        messages.error(request, "No tienes permisos para ver esta página.")
        return redirect('index')

    # Filtramos productos que el vendedor haya publicado y aún no se hayan agotado
    productos = Product.objects.filter(vendedor=request.user)
    return render(request, 'products/list_my_products.html', {'productos': productos})


@login_required_with_message
def editar_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk, vendedor=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.stock = request.POST.get('stock', producto.stock)  # Actualizar el campo de stock
            producto.save()
            messages.success(request, "Producto editado con éxito.")
            return redirect('listar_productos_vendedor')
    else:
        form = ProductForm(instance=producto)

    return render(request, 'products/edit_product.html', {'form': form})


@login_required_with_message
def eliminar_producto(request, pk):
    producto = get_object_or_404(Product, pk=pk, vendedor=request.user)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado con éxito.")
        return redirect('listar_productos_vendedor')

    return render(request, 'products/delete_product.html', {'producto': producto})


@login_required_with_message
def marcar_como_vendido(request, pk):
    producto = get_object_or_404(Product, pk=pk, vendedor=request.user)
    if request.method == 'POST':
        producto.vendido = True
        producto.save()
        messages.success(request, "Producto marcado como vendido.")
        return redirect('listar_mis_productos')

    return render(request, 'products/mark_as_sold.html', {'producto': producto})

@login_required
def menu_vendedor(request):
    # Solo el vendedor puede acceder a esta vista
    if not request.user.is_seller:
        messages.error(request, "No tienes permisos para ver esta página.")
        return redirect('index')

    # Obtener todos los productos del vendedor
    productos = Product.objects.filter(vendedor=request.user)
    return render(request, 'products/seller_menu.html', {'productos': productos})

# views.py (proceso de compra)
@login_required
def finalizar_compra(request, product_id):
    producto = get_object_or_404(Product, pk=product_id)
    if producto.stock > 0:
        producto.stock -= 1
        producto.save()
        if producto.stock == 0:
            producto.delete()
        messages.success(request, "Producto comprado con éxito, llegará en 2 días.")
        return redirect('carrito')
    else:
        messages.error(request, "El producto ya no está disponible.")
        return redirect('carrito')

def casa_view(request):
    return render(request, 'products/categories/casa.html')

def otros_view(request):
    if request.method == 'POST':
        # Mensaje de éxito
        messages.success(request, "¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.xd")
        return redirect('products:otros')  # Redirige a la misma página después de enviar
    return render(request, 'products/categories/otros.html')

from users.forms import EditProfileForm

@login_required_with_message
def perfil_view(request):
    user = request.user  # Usuario logueado
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('products:perfil')  # Redirigir al perfil actualizado
    else:
        form = EditProfileForm(instance=user)
    
    context = {'form': form}
    return render(request, 'products/categories/perfil.html', context)


from django.contrib.auth.decorators import login_required
from orders.models import PurchaseHistory

@login_required_with_message
def articulos_view(request):
    purchases = PurchaseHistory.objects.filter(user=request.user).order_by('-purchased_at')
    return render(request, 'products/categories/articulos.html', {'purchases': purchases})