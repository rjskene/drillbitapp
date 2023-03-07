import pandas as pd
from rest_framework import serializers

from drillbit_dj.project import ProjectListSerializer
from products.models import Rig, Cooling, HeatRejection, RejectionCurve, Electrical, \
    WeatherStation, WeatherData

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
            'capacity',
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
            'capacity',
            'design_dry_bulb',
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
            'capacity',
            'pue',
            'price',
        )
        list_serializer_class = ProjectListSerializer

class RejectionCurveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectionCurve
        fields = '__all__'

class RejectionCurveForProductSerializer(serializers.ModelSerializer):
    curve = RejectionCurveSerializer(read_only=True)

    class Meta:
        model = HeatRejection
        fields = (
            'id',
            'name',
            'curve',
        )
        read_only_fields = ('id', 'name', 'curve')

class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStation
        fields = '__all__'

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'

def expected_loss_from_insufficient_cooling_capacity(
    reward, difficulty,
    station, rig, rejection,
    n_coolers,
    ):
    station_dry_bulb = WeatherData.objects.get(station=station)
    dry_bulb = pd.DataFrame(station_dry_bulb.data)
    rej_curve = pd.DataFrame(rejection.curve.raw)

    df = pd.merge(rej_curve, dry_bulb, left_on='Ambient Temp (F)', right_on='Dry-Bulb °F', how='inner')
    df = df.drop('Dry-Bulb °F', axis=1)

    df.loc[:, 'Hash Rate per Cooler'] = df['Capacity (W)'] / rig.efficiency # W / W / TH / s
    df.loc[:, 'Number of Coolers'] = n_coolers

    df.loc[:, 'Project Hash Rate'] = df['Number of Coolers'] * df['Hash Rate per Cooler']
    df.loc[:, 'Project Hashes per Block'] = df['Project Hash Rate'] * (10 * 60)
    df.loc[:, 'Win Share'] = df['Project Hashes per Block'] / (2**32 * difficulty)

    df.loc[:, 'Frequency %'] = df['Cumulative Frequency %'] - df['Cumulative Frequency %'].shift(1).fillna(0)
    df.loc[df.index[-1], 'Frequency %'] = 100 - df.loc[df.index[-1], 'Cumulative Frequency %']
    df.loc[:, 'Expected BTC Earned per Block'] = df['Win Share'] * reward
    df.loc[:, 'Expected BTC Earned, Annual'] = df['Expected BTC Earned per Block'] * 6 * 24 * 365
    df['Weighted Expected BTC Earned, Annual'] = df['Expected BTC Earned, Annual'] * df['Frequency %'] / 100

    expected_loss = df.loc[df.index[0], 'Expected BTC Earned, Annual'] - df['Weighted Expected BTC Earned, Annual'].sum()
    
    return expected_loss