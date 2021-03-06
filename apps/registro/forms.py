from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#Carga el formato de los registros en la vista
class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
                'username',
                'first_name',
                'last_name',
            ]
        labels = {
                'username': 'Nombre de Usuario',
                'first_name':'Nombre',
                'last_name': 'Apellido',
            }