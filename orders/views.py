from django.shortcuts import render, redirect
from carts.utils import get_or_create_cart
from .models import Order
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = cart.order  # Obtenemos la orden asociada al carrito

    # Si la orden no existe, creamos una nueva
    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)
    if order:
        request.session['order_id'] = order.order_id

    # Pasar los productos del carrito junto con la orden al template
    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'cart_products': cart.cartproducts_set.all(),  # Enviando los productos del carrito
        'breadcrumb': breadcrumb()
    })

