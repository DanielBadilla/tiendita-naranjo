import uuid
from enum import Enum
from django.db import models
from users.models import User
from carts.models import Cart, CartProducts
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models import JSONField


class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'


choices = [(tag, tag.value) for tag in OrderStatus]


# Modelo de Orden
class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, choices=choices, default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=5, max_digits=8, decimal_places=0)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    products_data = JSONField(default=dict)  # Almacenar productos y cantidades como JSON

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def __str__(self):
        return self.order_id
    

    def get_total(self):
        """
        Calcula el total de la orden sumando los productos y el envío.
        """
        return sum(item['total'] for item in self.products_data) + int(self.shipping_total)

    def save_products(self):
        """
        Guarda una copia de los productos del carrito en el campo JSONField.
        """
        if self.cart:
            self.products_data = [
                {
                    'title': cp.product.title,
                    'quantity': cp.quantity,
                    'price': int(cp.product.price),
                    'total': int(cp.quantity) * int(cp.product.price)
                }
                for cp in self.cart.cartproducts_set.all()
            ]
            self.total = self.get_total()  # Calcula el total después de guardar los productos
        self.save()


# Señales para configurar el ID de la orden y el total
def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    if not instance.products_data:
        instance.save_products()

def update_total(self):
    self.total = self.get_total()
    self.save()


# Conectar las señales
pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)

from django.db import models
from django.conf import settings
from products.models import Product

class PurchaseHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchase_history")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.user.username} - {self.product.title} x{self.quantity}"

class Review(models.Model):
    EXPERIENCE_CHOICES = [
        ('muy_bueno', 'Muy Bueno'),
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
        ('malo', 'Malo'),
        ('muy_malo', 'Muy Malo'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    gusto_producto = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='regular')
    informacion_producto = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='regular')
    experiencia_pagina = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='regular')
    comentarios_adicionales = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.user.username} sobre {self.product.title}"