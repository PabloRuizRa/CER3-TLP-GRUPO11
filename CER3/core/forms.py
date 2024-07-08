from django import forms
from .models import RegistroProduccion
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegistroProduccionForm(forms.ModelForm):
    class Meta:
        model = RegistroProduccion
        fields = ['operador', 'turno', 'combustible', 'litros_producidos']

    fecha_produccion = forms.DateField(
        initial=timezone.now().date(),
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    hora_registro = forms.TimeField(
        initial=timezone.now().time(),
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_produccion'].widget.attrs['readonly'] = True
        self.fields['hora_registro'].widget.attrs['readonly'] = True


class Creacion_de_usuario(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'group')