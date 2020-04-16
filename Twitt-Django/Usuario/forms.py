from django.contrib.auth.models import User
from django import forms
from registration import forms as RegistrationForms



class UserRegisterForm(RegistrationForms.RegistrationFormUniqueEmail):
    """ Formulario para registro de usuarios extension de registration.forms.RegistrationFormUniqueEmail,
        el cual permite el registro con email y username unicos (no repetidos) caracteristicas:

        1. Nombre de usuario unico
        2. Email Unico
        3. Mensajes de errores ya establecidos
        4. Solicita campos de nombre y apellidos
    """
    class Meta:
        #Estableciendo modelo a usar
        model = User
        #Estableciendo campos a usar
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

        #Estableciendo cadena a mostrar en el atributo
        labels = {
            # 'username': forms.TextInput(attrs={'class' : 'form-control'}, requerid=True),
            'first_name': 'Nombre*',
            'last_name': 'Apellidos*',
            # 'email': forms.EmailInput(attrs={'class' : 'form-control'}, requerid=True),
            # 'password1': forms.PasswordInput(attrs={'class' : 'form-control'}, requerid=True),
            # 'password2': forms.PasswordInput(attrs={'class' : 'form-control'}, requerid=True),
        }
        #Estableciendo configuracion de campos first_name y last_name como requeridos
        widgets = {
            #'username': forms.TextInput(attrs={'class' : 'form-control'}, requerid=True),
            'first_name': forms.TextInput(attrs={'class' : 'form-control', 'required':''}),
            'last_name': forms.TextInput(attrs={'class' : 'form-control', 'required':''}),
            #'email': forms.EmailInput(attrs={'class' : 'form-control'}, requerid=True),
            #'password1': forms.PasswordInput(attrs={'class' : 'form-control'}, requerid=True),
            #'password2': forms.PasswordInput(attrs={'class' : 'form-control'}, requerid=True),
        }