from products.models import Product
from django.shortcuts import redirect, get_object_or_404, render
from .models import Cart 
from .utils import get_or_create_cart
from .models import CartProducts
from django.contrib.auth.decorators import login_required  # Importar el decorador login_required
from django.contrib import messages  # Importar para mostrar mensajes al usuario
from .forms import DireccionEntregaForm  # Importar el formulario de dirección
from orders.models import OrderStatus



# Create your views here.

def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
        #mandando el objeto cart al template
        'cart':cart
    })

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
            messages.success(request, "Producto comprado con éxito, llegará en X días.")
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


from orders.models import Order
from carts.utils import get_or_create_cart


@login_required
def confirmacion_compra(request):
    cart = get_or_create_cart(request)
    checkout_data = request.session.get('checkout_data')

    if not checkout_data:
        messages.error(request, "Por favor ingrese los datos de envío")
        return redirect('checkout')

    if request.method == 'POST':
        # Crear o asociar la orden al carrito actual
        order, created = Order.objects.get_or_create(
            user=request.user,
            cart=cart,
            defaults={
                'status': OrderStatus.CREATED.value,  # Estado inicial
                'shipping_total': 5  # Esto puedes cambiarlo según lo que necesites
            }
        )

        # Actualizar el total de la orden
        order.update_total()

        # Descontar el stock de los productos en el carrito
        for item in cart.cartproducts_set.all():
            item.product.stock -= item.quantity
            if item.product.stock < 0:
                item.product.stock = 0
            item.product.save()

        # Limpiar el carrito después de confirmar la compra
        cart.products.clear()

        # Cambiar estado de la orden a "COMPLETED"
        order.status = OrderStatus.COMPLETED.value
        order.save()

        messages.success(request, "Compra realizada con éxito.")
        return redirect('index')  # Redirigir al historial de compras

    return render(request, 'carts/confirmacion.html', {
        'cart': cart,
        'checkout_data': checkout_data,
        'cart_products': cart.cartproducts_set.all()
    })











