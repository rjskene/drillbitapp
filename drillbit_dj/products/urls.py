from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('rig', views.RigViewSet, basename='rig') 
router.register('cooling', views.CoolingViewSet, basename='cooling') 
router.register('heat-rejection', views.HeatRejectionViewSet, basename='heat-rejection')
router.register('heat-rejection-curve', views.RejectionCurveForProductViewSet, basename='heat-rejection-curve')
router.register('electrical', views.ElectricalViewSet, basename='electrical')
router.register('weather-stations', views.WeatherStationViewSet, basename='weather-station')
router.register('weather-data', views.WeatherDataViewSet, basename='weather-data')

urlpatterns = [
    path('weather-stations/regions/', views.get_weather_station_regions, name='weather-station-regions'),
    path('heat-rejection/temperature-impact/', views.RejectionTemperatureImpactView.as_view(), name='heat-rejection-temperature-impact'),
    path('heat-rejection/temperature-payback/', views.RejectionTemperaturePaybackView.as_view(), name='heat-rejection-temperature-payback'),
]

urlpatterns += router.urls