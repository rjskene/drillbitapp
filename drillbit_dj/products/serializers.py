from rest_framework import serializers

from drillbit_dj.project import ProjectListSerializer
from products.models import Rig, Cooling, HeatRejection, RejectionCurve, Electrical

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
            'power',
            'pue',
            'price',
            'number_of_rigs',
        )
        list_serializer_class = ProjectListSerializer
            
class HeatRejectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates
    curve_id = serializers.PrimaryKeyRelatedField(source='curve.id', queryset=RejectionCurve.objects.all())
    curve = serializers.SerializerMethodField(source='curve')

    class Meta:
        model = HeatRejection
        fields = (
            'id',
            'name', 
            'power',
            'pue',
            'price',
            'curve_id',
            'curve'
        )
        list_serializer_class = ProjectListSerializer
    
    def get_curve(self, obj):
        return (obj.curve.a, obj.curve.b)

class ElectricalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates

    class Meta:
        model = Electrical
        fields = (
            'id',
            'name',
            'power',
            'pue',
            'price',
        )
        list_serializer_class = ProjectListSerializer
    