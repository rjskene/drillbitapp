import datetime as dt
from rest_framework import viewsets, status
from rest_framework.response import Response

from .apps import btc

from .models import BlockSchedule, BitcoinPrice, \
    TransactionFees, HashRate, Environment
from .serializers import BlockScheduleSerializer, BitcoinPriceSerializer, \
    TransactionFeesSerializer, HashRateSerializer, EnvironmentSerializer

class EnvironmentViewSetMixin:
    def _finish_create(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer(self, *args, **kwargs):
        """
        Override the default serializer to pass in the bitcoin utility
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        return serializer_class(*args, bitcoin_utility=btc, **kwargs) # sneak in the bitcoin utility here

class BlockScheduleViewSet(EnvironmentViewSetMixin, viewsets.ModelViewSet):
    serializer_class = BlockScheduleSerializer
    queryset = BlockSchedule.objects.all()
    model = BlockSchedule

    def create(self, request, *args, **kwargs):     
        assert not isinstance(request.data, list), 'Bulk create not supported'
        data = request.data
        return self._finish_create(data)

class BitcoinPriceViewSet(EnvironmentViewSetMixin, viewsets.ModelViewSet):
    serializer_class = BitcoinPriceSerializer
    queryset = BitcoinPrice.objects.all()
    model = BitcoinPrice

    def create(self, request, *args, **kwargs):     
        assert not isinstance(request.data, list), 'Bulk create not supported'
        return self._finish_create(request.data)

class TransactionFeesViewSet(EnvironmentViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TransactionFeesSerializer
    queryset = TransactionFees.objects.all()
    model = TransactionFees

    def create(self, request, *args, **kwargs):     
        assert not isinstance(request.data, list), 'Bulk create not supported'
        return self._finish_create(request.data)

class HashRateViewSet(EnvironmentViewSetMixin, viewsets.ModelViewSet):
    serializer_class = HashRateSerializer
    queryset = HashRate.objects.all()
    model = HashRate

class EnvironmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnvironmentSerializer
    queryset = Environment.objects.all()

import json
from django.http import HttpResponse
def get_current_state(request):
    if 'update' in request.GET:
        update = json.loads(request.GET['update'])
        if update:
            btc.update_meta()

    return HttpResponse(btc.summary().to_json(), content_type='application/json')
