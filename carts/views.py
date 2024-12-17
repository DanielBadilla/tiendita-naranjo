from products.models import Product
from django.shortcuts import redirect, get_object_or_404, render
from .models import Cart 
from .utils import get_or_create_cart
from .models import CartProducts
from django.contrib.auth.decorators import login_required  # Importar el decorador login_required
from django.contrib import messages  # Importar para mostrar mensajes al usuario
from .forms import DireccionEntregaForm  # Importar el formulario de dirección
from orders.models import OrderStatus
from orders.models import Order
from django.urls import reverse
# Create your views here.

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
def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
        #mandando el objeto cart al template
        'cart':cart
    })
    
@login_required_with_message
def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock >= quantity:
        # Añadir al carrito
        cart_product = CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)
        messages.success(request, "Producto añadido al carrito.")
    else:
        messages.error(request, "No hay suficiente stock disponible.")
    
    return render(request, 'carts/add.html', {
        'quantity': quantity,
        'product': product,
        'cp': cart_product
    })
    
@login_required
def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    
    # Eliminar el producto del carrito
    cart.products.remove(product)

    return redirect('carts:cart')

@login_required
def finalizar_compra(request):
    cart = get_or_create_cart(request)

    if request.method == 'POST':
        direccion_form = DireccionEntregaForm(request.POST)
        if direccion_form.is_valid():
            # Procesar la compra, descontar el stock y mostrar el mensaje de éxito.
            for item in cart.cartproducts_set.all():
                item.product.stock -= item.quantity
                item.product.save()
                if item.product.stock == 0:
                    item.product.delete()  # Si el stock llega a 0, eliminamos el producto.

            # Limpiar el carrito después de la compra.
            cart.products.clear()

            # Mensaje de éxito y redirección a la página principal
            messages.success(request, "Producto comprado con éxito, llegará en 2 días.")
            return redirect('index')
    else:
        direccion_form = DireccionEntregaForm()

    return render(request, 'carts/checkout.html', {
        'cart': cart,
        'direccion_form': direccion_form
    })



    
@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    user = request.user  # Obtener el usuario logueado

    if request.method == 'POST':
        direccion_form = DireccionEntregaForm(request.POST, user=user)
        if direccion_form.is_valid():
            # Guardar los datos temporalmente en la sesión
            request.session['checkout_data'] = direccion_form.cleaned_data
            return redirect('confirmacion_compra')
    else:
        # Prellenar los datos del usuario
        direccion_form = DireccionEntregaForm(user=user)

    return render(request, 'carts/checkout.html', {
        'cart': cart,
        'direccion_form': direccion_form
    })


from orders.models import PurchaseHistory  # Importamos el nuevo modelo


@login_required
def confirmacion_compra(request):
    # Obtener el carrito asociado al usuario
    cart = get_or_create_cart(request)  # Asegúrate de tener esta función implementada
    checkout_data = request.session.get('checkout_data')  # Datos de envío desde la sesión

    # Si no hay datos de checkout, redirigir al formulario
    if not checkout_data:
        messages.error(request, "Por favor confirme los datos de envío.")
        return redirect('checkout')

    # Si el método es POST, procesar la compra
    if request.method == 'POST':
        # Crear la orden o asociarla al carrito
        order, created = Order.objects.get_or_create(
            user=request.user,
            cart=cart,
            defaults={'status': OrderStatus.CREATED.value, 'shipping_total': 5}
        )
        order.update_total()  # Actualizar el total de la orden

        # Registrar historial de compras y descontar stock
        for item in cart.cartproducts_set.all():
            PurchaseHistory.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total=item.quantity * item.product.price
            )
            # Actualizar stock del producto
            item.product.stock -= item.quantity
            if item.product.stock < 0:
                item.product.stock = 0
            item.product.save()

        # Limpiar el carrito después de confirmar la compra
        cart.products.clear()
        order.status = OrderStatus.COMPLETED.value
        order.save()

        messages.success(request, "Compra realizada con éxito. Llegará dentro de 2 días.")
        return redirect('index')  # Redirigir al inicio o a un historial de compras

    # Preparar el contexto para la vista de confirmación
    products = cart.cartproducts_set.all()  # Obtener los productos en el carrito
    context = {
        'cart': cart,
        'checkout_data': checkout_data,
        'cart_products': products,  # Pasar los productos al template
    }
    return render(request, 'carts/confirmacion.html', context)