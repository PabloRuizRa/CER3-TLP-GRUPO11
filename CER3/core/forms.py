from django import forms
from .models import RegistroProduccion
from django.utils import timezone

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
