from rest_framework import serializers

from drillbit_dj.project import ProjectListSerializer
from products.models import Rig, Cooling, HeatRejection, Electrical

class RigSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates
    name = serializers.SerializerMethodField()

    class Meta:
        model = Rig
        fields = (
            'id',
            'name', 'make', 'model', 'generation', 'manufacturer', 
            'hash_rate', 'power', 'buffer',
            'price'
        )
        list_serializer_class = ProjectListSerializer
    
    def name(self, obj):
        return obj.name

class CoolingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates

    class Meta:
        model = Cooling
        fields = (
            'id',
            'name', 
            'pue',
            'price'
        )
        list_serializer_class = ProjectListSerializer
            
class HeatRejectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates

    class Meta:
        model = HeatRejection
        fields = (
            'id',
            'name', 
            'pue',
            'price'
        )
        list_serializer_class = ProjectListSerializer
    
class ElectricalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates
    name = serializers.SerializerMethodField()

    class Meta:
        model = Electrical
        fields = (
            'id',
            'name', 
            'pue',
            'price'
        )
        list_serializer_class = ProjectListSerializer
    
    def name(self, obj):
        return obj.name
