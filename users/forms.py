from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True, min_length=4, max_length=50, label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        required=True, label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        required=True, label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite Contraseña'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'El email {email} ya se encuentra en uso')
        return email 

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Las contraseñas no coinciden')

    def save(self, commit=True, is_seller=False):
        # No guarda automáticamente, para permitir modificaciones
        user = CustomUser(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
        )
        user.set_password(self.cleaned_data.get('password'))
        user.is_seller = is_seller  # Define si es vendedor o no
        if commit:
            user.save()
        return user

# Formulario para Vendedores
class RegisterSellerForm(RegisterForm):
    def save(self, commit=True):
        # Usa el método `save` del padre y pasa `is_seller=True`
        return super().save(commit=commit, is_seller=True)

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Nombre de Usuario"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario','value': ''})
    )
    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    error_messages = {
        'invalid_login': _(
            "Nombre de usuario o contraseña incorrectos. Verifica las mayúsculas y vuelve a intentar."
        ),
        'inactive': _("Esta cuenta está inactiva."),
    }
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'descripcion', 'region', 'comuna']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'descripcion': 'Descripción',
            'region' : 'Region',
            'comuna' : 'Comuna',
            }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'region': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Region'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comuna'}),
        }
