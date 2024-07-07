from django.contrib import admin
from django.urls import path, include
from core import views as registro_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registro_views.registrar_produccion, name='home'),  # Esto es solo un ejemplo, ajusta según sea necesario
    path('registro/registrar/', registro_views.registrar_produccion, name='registrar_produccion'),
    path('registro/exito/', registro_views.registro_exitoso, name='registro_exitoso'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('rest_framework.urls')),
]
