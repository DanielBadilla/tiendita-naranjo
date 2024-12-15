import uuid
from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.conf import settings  # Para AUTH_USER_MODEL

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    products = models.ManyToManyField(Product, through='CartProducts')
    subtotal = models.IntegerField(default=0)  # Cambiado a IntegerField para usar enteros
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.05  # Comisión del 5%

    def __str__(self):
        return self.cart_id

    def update_totals(self):
        self.update_subtotal()
        self.update_total()
        if self.order:  # Actualiza el pedido asociado si existe
            self.order.update_total()

    def update_subtotal(self):
        # Calcula el subtotal basado en la cantidad y precio de los productos en el carrito
        self.subtotal = sum(
            cp.quantity * cp.product.price for cp in self.products_related()
        )
        self.save()

    def update_total(self):
        # Calcula el total con la comisión aplicada
        self.total = int(self.subtotal * (1 + Cart.FEE))
        self.save()

    def products_related(self):
        # Optimiza la consulta de productos relacionados
        return self.cartproducts_set.select_related('product')

    @property
    def order(self):
        # Devuelve el primer pedido relacionado
        return self.order_set.first()

class CartProductsManager(models.Manager):
    def create_or_update_quantity(self, cart, product, quantity=1):
        obj, created = self.get_or_create(cart=cart, product=product)
        if not created:
            quantity = obj.quantity + quantity
        obj.update_quantity(quantity)
        return obj

class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartProductsManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()

# Señales (Callbacks)
def set_cart_id(sender, instance, *args, **kwargs):
    # Si el carrito no tiene un identificador único, se genera uno
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def post_save_update_totals(sender, instance, *args, **kwargs):
    # Actualiza los totales del carrito al guardar un CartProduct
    instance.cart.update_totals()

def m2m_update_totals(sender, instance, action, *args, **kwargs):
    # Actualiza los totales al modificar productos en el ManyToManyField
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_totals()

# Conexión de las señales
pre_save.connect(set_cart_id, sender=Cart)
post_save.connect(post_save_update_totals, sender=CartProducts)
m2m_changed.connect(m2m_update_totals, sender=Cart.products.through)
