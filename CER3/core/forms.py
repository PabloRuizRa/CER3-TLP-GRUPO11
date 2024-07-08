from django import forms
from .models import RegistroProduccion, RegistroAuditoriaActualizacion
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegistroProduccionForm(forms.ModelForm):
    class Meta:
        model = RegistroProduccion
        fields = ['operador', 'turno', 'combustible', 'litros_producidos']

    fecha_produccion = forms.DateField(
        initial=timezone.now().date(),
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    hora_registro = forms.TimeField(
        initial=timezone.now().time(),
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['fecha_produccion'].widget.attrs['readonly'] = True
        self.fields['hora_registro'].widget.attrs['readonly'] = True



class Creacion_de_usuario(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'group')

class RegistroAuditoriaActualizacionForm(forms.ModelForm):
    class Meta:
        model = RegistroAuditoriaActualizacion
        fields = ['detalle']