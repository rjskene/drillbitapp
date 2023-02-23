import json
import pandas as pd
from rest_framework import serializers

from drillbit_dj.project import ProjectListSerializer, GetOrCreateSerializerMixin
from environment.models import Environment, BlockSchedule, BitcoinPrice, TransactionFees, HashRate

class JSONConversionField(serializers.JSONField):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, value):
        if isinstance(value, dict):
            return value
        else:
            return json.loads(value)

class BitcoinUtilityInitMixin:
    def __init__(self, *args, bitcoin_utility=None, **kwargs):
        self.btc = bitcoin_utility
        super().__init__(*args, **kwargs)

class EnvironmentFieldsMixin:
    blocks = serializers.PrimaryKeyRelatedField(queryset=BlockSchedule.objects.all(), read_only=False)
    data = JSONConversionField(source='json', read_only=True)

class EnvironmentCreateMixin(GetOrCreateSerializerMixin):
    def create(self, validated_data):
        """
        Locates the block schedule and uses it to generate a forecast.

        The forecast is then serialized into a JSON string and stored in the
        database, if it doesn't exist already first.
        """
        blocks = validated_data.pop('blocks')
        periods = BlockScheduleSerializer(blocks, bitcoin_utility=self.btc).to_schedule().period
        forecast = self.btc.forecast(periods=periods, **validated_data)
        obj = self._schedule_create(forecast, validated_data, blocks=blocks)

        return obj

class BlockScheduleSerializer(
    BitcoinUtilityInitMixin,
    GetOrCreateSerializerMixin, 
    serializers.ModelSerializer
    ):
    data = JSONConversionField(source='json', read_only=True)

    class Meta:
        model = BlockSchedule
        fields = (
            'id', 'start_date', 'last_epoch', 'data'
        )
        list_serializer_class = ProjectListSerializer
        validators = []  # Removes the "unique together" constraint.

    def create(self, validated_data):
        """
        Generates block schedule and serializes it into a JSON string.

        """
        try:
            obj = self._try_get(validated_data)
        except self.Meta.model.DoesNotExist:
            schedule = self.btc.generate_block_schedule(
                validated_data['start_date'], 
                validated_data['last_epoch']
            ).reset_index()
            schedule.period = schedule.period.astype(str)
            obj = self._schedule_create(schedule, validated_data)

        return obj

    def to_schedule(self, with_period_index=False):
        """
        Converts the JSON string into a pandas DataFrame.

        Parameters
        ----------
        with_periods : bool, optional
            If True, the period column is returned as a pandas PeriodIndex.
            Otherwise, the period column is returned as a string. Default: False.

        Returns
        -------
        df : pandas.DataFrame
            The block schedule as a DataFrame.
        """
        df = pd.DataFrame(self.data['data'])
        if with_period_index:
            df = df.set_index('period')
            df.index = pd.to_datetime(df.index).to_period()

        return df

class BitcoinPriceSerializer(
    BitcoinUtilityInitMixin,
    EnvironmentCreateMixin, 
    serializers.ModelSerializer
    ):
    blocks = serializers.PrimaryKeyRelatedField(queryset=BlockSchedule.objects.all())
    data = JSONConversionField(source='json', read_only=True)

    class Meta:
        model = BitcoinPrice
        fields = (
            'id',
            'blocks', 'model', 'initial', 'mean', 'volatility', 'data'
        )
        list_serializer_class = ProjectListSerializer
        validators = []  # Removes the "unique together" constraint.

    def to_schedule(self):
        return pd.DataFrame(self.data['data'])

class TransactionFeesSerializer(
    BitcoinUtilityInitMixin,
    EnvironmentCreateMixin, 
    serializers.ModelSerializer
    ):
    blocks = serializers.PrimaryKeyRelatedField(queryset=BlockSchedule.objects.all())
    data = JSONConversionField(source='json', read_only=True)

    class Meta:
        model = TransactionFees
        fields = (
            'id',
            'blocks', 'model', 'initial', 'mean', 'volatility', 'data'
        )
        list_serializer_class = ProjectListSerializer
        validators = []  # Removes the "unique together" constraint.

    def to_schedule(self):
        return pd.DataFrame(self.data['data'])

class HashRateSerializer(
    BitcoinUtilityInitMixin,
    EnvironmentCreateMixin, 
    serializers.ModelSerializer
    ):
    blocks = serializers.PrimaryKeyRelatedField(queryset=BlockSchedule.objects.all())
    data = JSONConversionField(source='json', read_only=True)

    class Meta:
        model = HashRate
        fields = (
            'id',
            'blocks', 'model', 'initial', 'mean', 'volatility', 'data'
        )
        list_serializer_class = ProjectListSerializer
        validators = []  # Removes the "unique together" constraint.

    def to_schedule(self):
        return pd.DataFrame(self.data['data'])

class EnvironmentSerializer(serializers.ModelSerializer):
    block_schedule = serializers.PrimaryKeyRelatedField(queryset=BlockSchedule.objects.all())
    bitcoin_price = serializers.PrimaryKeyRelatedField(queryset=BitcoinPrice.objects.all())
    transaction_fees = serializers.PrimaryKeyRelatedField(queryset=TransactionFees.objects.all())
    hash_rate = serializers.PrimaryKeyRelatedField(queryset=HashRate.objects.all())

    class Meta:
        model = Environment
        fields = (
            'id',
            'name',
            'block_schedule',
            'bitcoin_price', 
            'transaction_fees', 
            'hash_rate'
        )

class EnvironmentParamSerializer:
    pass