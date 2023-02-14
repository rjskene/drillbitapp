from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('rig', views.RigViewSet, basename='rig') 
router.register('cooling', views.CoolingViewSet, basename='cooling') 
router.register('heat-rejection', views.HeatRejectionViewSet, basename='heat-rejection') 
router.register('electrical', views.ElectricalViewSet, basename='electrical') 

urlpatterns = [
]

urlpatterns += router.urls