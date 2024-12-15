# models.py (en la carpeta products)
import uuid
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from users.models import CustomUser  # Importamos el modelo de usuario personalizado

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad disponible")
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=False, blank=False)
    vendedor = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='productos')
    vendido = models.BooleanField(default=False, verbose_name="Estado Vendido")  # Añadir el campo vendido

    def __str__(self):
        return self.title

# Callback para generar un slug único basado en el título
def set_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        while Product.objects.filter(slug=slug).exists():
            slug = slugify("{}-{}".format(instance.title, str(uuid.uuid4())[:8]))
        instance.slug = slug

# Antes de que un objeto Product se almacene, ejecuta el callback set_slug
pre_save.connect(set_slug, sender=Product)
