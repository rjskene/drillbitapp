from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('block-schedule', views.BlockScheduleViewSet, basename='block-schedule') 
router.register('bitcoin-price', views.BitcoinPriceViewSet, basename='bitcoin-price')
router.register('transaction-fees', views.TransactionFeesViewSet, basename='transaction-fees')
router.register('hash-rate', views.HashRateViewSet, basename='hash-rate') 
router.register('environment', views.EnvironmentViewSet, basename='environment')

urlpatterns = [
]

urlpatterns += router.urls