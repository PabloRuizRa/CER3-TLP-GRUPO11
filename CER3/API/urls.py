from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroProduccionViewSet

router = DefaultRouter()
router.register(r'registros', RegistroProduccionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]