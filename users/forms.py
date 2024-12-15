from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=50,label='Usuario',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'id': 'username',
                                    'placeholder': 'Username'
                                    ,'value': ''}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
                                    'class': 'form-control',
                                    'id': 'email',
                                    'placeholder': 'Email'
                                    ,'value': ''}))
    password = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'id': 'password',
                                    'placeholder': 'Contraseña'}))
    password2 = forms.CharField(required=True, label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'id': 'password2',
                                    'placeholder': 'Repite Contraseña'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Verifica si el usuario ya existe en la base de datos
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica si el email ya existe en la base de datos
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('El email {} ya se encuentra en uso'.format(email))

        return email 

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')

    def save(self):
        return CustomUser.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )

class RegisterSellerForm(RegisterForm):
    def save(self):
        user = super().save()
        user.is_seller = True
        user.save()
        return user

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
