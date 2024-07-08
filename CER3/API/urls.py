from django.urls import path, include
from rest_framework.routers import DefaultRouter
from API.views import RegistroProduccionViewSet, ProduccionPorCombustiblePlantaViewSet, ProduccionPorCombustibleFiltradaViewSet

router = DefaultRouter()
router.register(r'registros', RegistroProduccionViewSet)
router.register(r'produccion-por-combustible-planta', ProduccionPorCombustiblePlantaViewSet, basename='produccion-por-combustible-planta')
router.register(r'produccion-por-combustible-filtrada', ProduccionPorCombustibleFiltradaViewSet, basename='produccion-por-combustible-filtrada')

urlpatterns = [
    path('', include(router.urls)),
]