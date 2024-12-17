from django.shortcuts import render, redirect
from carts.utils import get_or_create_cart
from orders.models import Order, OrderStatus
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from django.contrib import messages
# Create your views here.
from .forms import ReviewForm, Review
from .models import PurchaseHistory
from products.models import Product

@login_required
def order(request):
    cart = get_or_create_cart(request)

    # Verifica si ya existe una orden para este carrito y usuario
    order = Order.objects.filter(cart=cart, user=request.user).first()

    # Si no existe la orden, créala
    if not order:
        order = Order.objects.create(
            cart=cart,
            user=request.user,
            status=OrderStatus.CREATED.value,
            shipping_total=5
        )
        order.update_total()

    # Pasar la orden al template
    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'cart_products': cart.cartproducts_set.all()
    })

from products.models import Product
from orders.models import Order, PurchaseHistory, OrderStatus
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from carts.utils import get_or_create_cart


@login_required
def leave_review(request):
    cart = get_or_create_cart(request)  # Obtener el carrito actual
    products = cart.cartproducts_set.all()  # Productos en el carrito

    if not products:  # Si el carrito está vacío
        messages.error(request, "No hay productos para evaluar.")
        return redirect('index')

    if request.method == 'POST':
        forms = [ReviewForm(request.POST, prefix=str(item.product.id)) for item in products]
        if all(form.is_valid() for form in forms):
            for item, form in zip(products, forms):
                review = form.save(commit=False)
                review.product = item.product
                review.user = request.user
                review.save()

            # Registrar la compra después de completar las evaluaciones
            order, created = Order.objects.get_or_create(
                user=request.user,
                cart=cart,
                defaults={'status': OrderStatus.CREATED.value, 'shipping_total': 5}
            )
            order.update_total()

            # Guardar historial de compras y descontar stock
            for item in products:
                PurchaseHistory.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total=item.quantity * item.product.price
                )
                # Reducir el stock
                item.product.stock -= item.quantity
                item.product.save()

            # Limpiar el carrito
            cart.products.clear()
            order.status = OrderStatus.COMPLETED.value
            order.save()

            # Redirigir a la página principal con mensaje
            messages.success(request, "¡Gracias por tu opinión! La compra ha sido confirmada.")
            return redirect('index')
    else:
        # Generar un formulario para cada producto
        forms = [ReviewForm(prefix=str(item.product.id)) for item in products]

    return render(request, 'orders/reviews/leave_review.html', {
        'forms': forms,
        'products': products
    })