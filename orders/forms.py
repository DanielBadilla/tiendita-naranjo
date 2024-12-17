from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['gusto_producto', 'informacion_producto', 'experiencia_pagina', 'comentarios_adicionales']
        widgets = {
            'gusto_producto': forms.Select(attrs={'class': 'form-control'}),
            'informacion_producto': forms.Select(attrs={'class': 'form-control'}),
            'experiencia_pagina': forms.Select(attrs={'class': 'form-control'}),
            'comentarios_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
