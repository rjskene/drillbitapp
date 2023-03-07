import json

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from drillbit_dj.project import BulkUpdateViewSetMixin
from .models import Rig, Cooling, HeatRejection, Electrical, WeatherStation, WeatherData
from .serializers import RigSerializer, CoolingSerializer, HeatRejectionSerializer, ElectricalSerializer, \
    RejectionCurveForProductSerializer, WeatherStationSerializer, WeatherDataSerializer

class RigViewSet(BulkUpdateViewSetMixin, viewsets.ModelViewSet):
    serializer_class = RigSerializer
    queryset = Rig.objects.all()
    model = Rig

class CoolingViewSet(BulkUpdateViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CoolingSerializer
    queryset = Cooling.objects.all()
    model = Cooling

class HeatRejectionViewSet(BulkUpdateViewSetMixin, viewsets.ModelViewSet):
    serializer_class = HeatRejectionSerializer
    queryset = HeatRejection.objects.all()
    model = HeatRejection

class ElectricalViewSet(BulkUpdateViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ElectricalSerializer
    queryset = Electrical.objects.all()
    model = Electrical

class RejectionCurveForProductViewSet(viewsets.ModelViewSet):
    serializer_class = RejectionCurveForProductSerializer
    queryset = HeatRejection.objects.all()
    model = HeatRejection

class WeatherStationViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherStationSerializer
    queryset = WeatherStation.objects.all()
    model = WeatherStation

class WeatherDataViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()
    model = WeatherData
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station']

def get_weather_station_regions(request):
    regions = WeatherStation.objects.values_list('region', flat=True).distinct()
    return HttpResponse(json.dumps(list(regions)), content_type ="application/json")

# def get_weather_data(request, type, variable, station_id):
