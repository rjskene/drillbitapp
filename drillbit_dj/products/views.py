import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drillbit_dj.project import BulkUpdateViewSetMixin
from .models import Rig, Cooling, HeatRejection, Electrical
from .serializers import RigSerializer, CoolingSerializer, HeatRejectionSerializer, ElectricalSerializer

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

