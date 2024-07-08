from django.contrib import admin
from django.urls import path, include
from core import views as registro_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registro_views.home, name='home'),  
    path('registro/', registro_views.registrar_produccion),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('rest_framework.urls')),
    path('crear_usuario/', registro_views.crear_usuario, name='crear_usuario'),
    path('logout/', registro_views.exit, name="exit"),
]
