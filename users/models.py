from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

#SI NO SE QUIERE EXTENDER EL MODELO USER A OTRO, SINO GENERAR UNO NOSOTROS SE PUEDE USAR EL ABSTRACT USER

class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=True, verbose_name="Es vendedor")
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    comuna = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    #CASCADE ES CUANDO UN USUARIO SEA ELIMINADO TAMBIEN SE ELIMINE SU PROFILE EN CASCADA
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
