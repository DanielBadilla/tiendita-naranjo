# forms.py (en la carpeta products)
from django import forms
from .models import Product  # Cambia Producto a Product para coincidir con el modelo actual

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'stock', 'image']  # Incluimos el campo 'stock' aquí
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad disponible'}),  # Añadimos el widget para 'stock'
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'stock', 'image', 'slug']  # Incluye el campo stock


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'stock', 'image', 'slug']  # Incluye el campo stock
