import numpy as np
import pandas as pd
import scipy.stats as scist
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

class RejectionTemperaturePaybackSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(queryset=WeatherStation.objects.all())
    rig = serializers.PrimaryKeyRelatedField(queryset=Rig.objects.all())
    price = serializers.FloatField()
    reward = serializers.FloatField()
    difficulty = serializers.FloatField()
    capacity = serializers.FloatField()

    class Meta:
        model = HeatRejection
        fields = (
            'station',
            'rig',
            'capacity',
            'price',
            'reward',
            'difficulty',
        )
        write_only_fields = ('station', 'rig', 'capacity', 'price', 'reward', 'difficulty')

    def create(self, validated_data):
        station = validated_data.pop('station')
        rig = validated_data.pop('rig')
        capacity = validated_data.pop('capacity')
        price = validated_data.pop('price')
        reward = validated_data.pop('reward')
        difficulty = validated_data.pop('difficulty')

        station_dry_bulb = WeatherData.objects.get(
            station=station, 
            type='Single-Variable Frequency',
            variable='Dry-Bulb',
        ).data

        datas = []
        for rejection in HeatRejection.objects.all():
            n_coolers = capacity / rejection.capacity

            df, expected_loss = expected_loss_from_insufficient_cooling_capacity(
                reward,
                difficulty,
                station_dry_bulb,
                rig.efficiency,
                rejection.curve.raw,
                n_coolers,
            )

            cost_of_coolers = n_coolers * rejection.price
            data = {
                'design_dry_bulb': rejection.design_dry_bulb,
                'cost_of_coolers': cost_of_coolers,
                'expected_loss': expected_loss
            }
            datas.append(data)

        df = pd.DataFrame(datas)
        df.loc[:, 'incremental_gain'] = -df.expected_loss.diff().fillna(0)
        df.loc[:, 'cumulative_gain'] = df.incremental_gain.cumsum()
        df.loc[:, 'incremental_cost'] = df.cost_of_coolers.diff().fillna(0)
        df.loc[:, 'cumulative_cost'] = df.incremental_cost.cumsum()
        df.loc[:, 'cumulative_gain_usd'] = df.cumulative_gain * price
        df.loc[:, 'payback'] = df.cumulative_cost / df.cumulative_gain_usd

        return df.fillna('-').to_dict('records')

class RejectionTemperatureImpactSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(queryset=WeatherStation.objects.all())
    rig = serializers.PrimaryKeyRelatedField(queryset=Rig.objects.all())
    rejection = serializers.PrimaryKeyRelatedField(queryset=HeatRejection.objects.all())
    reward = serializers.FloatField()
    difficulty = serializers.FloatField()
    capacity = serializers.FloatField()

    class Meta:
        model = HeatRejection
        fields = (
            'station',
            'rig',
            'rejection',
            'capacity',
            'reward',
            'difficulty',
        )
        write_only_fields = ('station', 'rig', 'rejection', 'capacity', 'reward', 'difficulty',)

    def create(self, validated_data):
        station = validated_data.pop('station')
        rig = validated_data.pop('rig')
        rejection = validated_data.pop('rejection')
        capacity = validated_data.pop('capacity')
        reward = validated_data.pop('reward')
        difficulty = validated_data.pop('difficulty')

        station_dry_bulb = WeatherData.objects.get(
            station=station, 
            type='Single-Variable Frequency',
            variable='Dry-Bulb',
        ).data

        n_coolers = capacity / rejection.capacity
        df, expected_loss = expected_loss_from_insufficient_cooling_capacity(
            reward,
            difficulty,
            station_dry_bulb,
            rig.efficiency,
            rejection.curve.raw,
            n_coolers,
        )
        return {
            'expected_loss': expected_loss,
            'data': df.to_dict('records'),
        }

class DryBulbSimulationSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(queryset=WeatherStation.objects.all())

    class Meta:
        model = WeatherData
        fields = (
            'station',
            'type',
            'variable',
            'units'

        )
        read_only_fields = ('type', 'variable', 'units')

    def create(self, validated_data):
        station = validated_data.pop('station')

        datas = WeatherData.objects.filter(
            station=station,
            type='Diurnal',
            variable='Dry-Bulb'
        )

        dfs = []
        months = []
        for data in datas:
            df = pd.DataFrame(data.data) \
                .set_index('Hour')
            month = pd.Period(data.period, freq='M', year=2022)
            months.append(month)
            dfs.append(df)

        df = pd.concat(dfs, keys=months, names=['Month', 'Hour']).sort_index() # this sort is very important!!!!!
        temps = df.values.reshape(-1, 24, 6) # 12, 24, 6 matrix where axis-3 is average, 10/25/50/75/90 percentiles

        temp_params = WeatherData.objects.get(
            station=station,
            type='Month-Hour-Params-Students-T',
            variable='Dry-Bulb',
        )
        temp_params = np.array(temp_params.data)

        temps_by_month = []
        for m in range(temps.shape[0]):
            month = pd.Period(freq='M', month=m+1, year=2022)
            temps_by_hr = np.zeros((24, month.days_in_month))
            for (hr,), mean_temp in np.ndenumerate(temps[m, :, 0]):
                df, var = temp_params[m, hr]
                mean_temp = temps[m, hr, 0]
                norm = scist.t(df, loc=mean_temp, scale=var)
                rvs = norm.rvs(month.days_in_month)
                temps_by_hr[hr] = np.clip(rvs, *norm.ppf([0.01, 0.99])) # enforces a clip on Student's T; this is just a patch ... should find better distributions
            
            temps_by_month += np.transpose(temps_by_hr).flatten().tolist() # transpose swaps the dimensions

        periods = pd.period_range(periods=len(temps_by_month), freq='H', end=month)
        return {
            'station': station.id,
            'periods': periods.strftime('%Y-%m-%d %H:%M'),
            'data': temps_by_month,
        }

def expected_loss_from_insufficient_cooling_capacity(
    reward, difficulty,
    station_dry_bulb, rig_efficiency, rejection_curve,
    n_coolers,
    ):
    dry_bulb = pd.DataFrame(station_dry_bulb)
    rej_curve = pd.DataFrame(rejection_curve)

    df = pd.merge(rej_curve, dry_bulb, left_on='Ambient Temp (F)', right_on='Dry-Bulb °F', how='inner')
    df = df.drop('Dry-Bulb °F', axis=1)

    df.loc[:, 'Hash Rate per Cooler'] = df['Capacity (W)'] / rig_efficiency # W / W / TH / s
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
    
    return df, expected_loss
