from .models import Cart

def get_or_create_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)
    return cart
