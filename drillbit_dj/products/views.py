import json

from django.http import HttpResponse
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from drillbit_dj.project import BulkUpdateViewSetMixin
from .models import Rig, Cooling, HeatRejection, Electrical, WeatherStation, WeatherData
from .serializers import RigSerializer, CoolingSerializer, HeatRejectionSerializer, ElectricalSerializer, \
    RejectionCurveForProductSerializer, WeatherStationSerializer, WeatherDataSerializer, \
    RejectionTemperatureImpactSerializer, RejectionTemperaturePaybackSerializer, \
    DryBulbSimulationSerializer

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

class RejectionCurveForProductViewSet(viewsets.ModelViewSet):
    serializer_class = RejectionCurveForProductSerializer
    queryset = HeatRejection.objects.all()
    model = HeatRejection

class RejectionTemperaturePaybackView(generics.CreateAPIView):
    serializer_class = RejectionTemperaturePaybackSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)

class RejectionTemperatureImpactView(generics.CreateAPIView):
    serializer_class = RejectionTemperatureImpactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)

class ElectricalViewSet(BulkUpdateViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ElectricalSerializer
    queryset = Electrical.objects.all()
    model = Electrical

class WeatherStationViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherStationSerializer
    queryset = WeatherStation.objects.all()
    model = WeatherStation

class WeatherDataViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()
    model = WeatherData
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station', 'type', 'variable', 'period']

    def list(self, request, *args, **kwargs):
        type = request.GET.get('type', None)

        if type == 'Simulation':
            station_id = request.GET.get('station', None)
            serializer = DryBulbSimulationSerializer(data={'station': station_id})
            serializer.is_valid()
            result = serializer.save()
            
            # result returned as an array to be consistent with other returns from `list`
            return Response([result])
        else:
            return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='get-types', name='Get Station Data Types')
    def get_types(self, request):
        variable = request.GET.get('variable', None)
        filter_kwargs = {}
        if variable:
            filter_kwargs['variable'] = variable
        types = WeatherData.objects.filter(**filter_kwargs).values_list('type', flat=True).distinct()
        return Response(list(types))

    @action(detail=False, methods=['get'], url_path='get-variables', name='Get Station Variable Types')
    def get_variables(self, request):
        type = request.GET.get('type', None)
        filter_kwargs = {}
        if type:
            filter_kwargs['variable'] = type

        variables = WeatherData.objects.values_list('variable', flat=True).distinct()
        return Response(list(variables))

    @action(detail=False, methods=['get'], url_path='get-periods', name='Get Station Data Periods')
    def get_periods(self, request):
        type = request.GET.get('type', None)
        variable = request.GET.get('variable', None)        
        
        filter_kwargs = {}
        if variable:
            filter_kwargs['variable'] = variable
        if type:
            filter_kwargs['type'] = type

        periods = WeatherData.objects.filter(**filter_kwargs).values_list('period', flat=True).distinct()
        return Response(list(periods))

    @action(detail=False, methods=['post'], url_path='dry-bulb-simulation', name='Dry Bulb Simulation')
    def dry_bulb_simulation(self, request, pk=None):
        """
        request.data should be of form {station: <station_id>}
        """
        station = self.get_object()
        serializer = DryBulbSimulationSerializer(data=request.data)
        serializer.is_valid()
        result = serializer.save()
        
        return Response(result)

def get_weather_station_regions(request):
    regions = WeatherStation.objects.values_list('region', flat=True).distinct()
    return HttpResponse(json.dumps(list(regions)), content_type ="application/json")

# def get_weather_data(request, type, variable, station_id):
