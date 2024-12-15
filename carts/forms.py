from django import forms

class DireccionEntregaForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre y Apellido", required=True)
    direccion = forms.CharField(max_length=200, label="Dirección de Entrega", required=True)
    region = forms.CharField(max_length=100, label="Región", required=True)
    comuna = forms.CharField(max_length=100, label="Comuna", required=True)
    telefono = forms.CharField(max_length=15, label="Teléfono de Contacto", required=True)
    metodo_pago = forms.ChoiceField(
        choices=[('tarjeta', 'Tarjeta de Crédito'), ('efectivo', 'Pago en Efectivo')],
        label="Método de Pago",
        required=True
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Prellenar campos con datos del perfil del usuario
            self.fields['nombre'].initial = f"{user.first_name} {user.last_name}"
            self.fields['direccion'].initial = user.direccion
            self.fields['region'].initial = user.region
            self.fields['comuna'].initial = user.comuna
            self.fields['telefono'].initial = user.telefono
