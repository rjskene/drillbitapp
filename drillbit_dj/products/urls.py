from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('rigs', views.RigViewSet, basename='rigs') 
router.register('cooling', views.CoolingViewSet, basename='cooling') 
router.register('rejection', views.HeatRejectionViewSet, basename='rejection') 
router.register('electrical', views.ElectricalViewSet, basename='electrical') 

urlpatterns = [
]

urlpatterns += router.urls