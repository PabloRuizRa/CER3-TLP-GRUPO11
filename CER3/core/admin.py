from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Planta, Combustible, RegistroProduccion

# Registrar Modelos en el Admin de Django
admin.site.register(Planta)
admin.site.register(Combustible)

# Configuración del modelo RegistroProduccion
class RegistroProduccionAdmin(admin.ModelAdmin):
    list_display = ('combustible', 'litros_producidos', 'fecha_produccion', 'turno', 'hora_registro', 'operador')
    list_filter = ('fecha_produccion', 'turno', 'operador')
    search_fields = ('combustible__nombre', 'operador__username')

admin.site.register(RegistroProduccion, RegistroProduccionAdmin)