import json
import pandas as pd
from rest_framework import serializers

from drillbit_dj.project import ProjectListSerializer, GetOrCreateSerializerMixin
from environment.models import BlockSchedule, BitcoinPrice, TransactionFees, HashRate

class JSONConversionField(serializers.JSONField):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, value):
        return json.loads(value)

class BitcoinUtilityInitMixin:
    def __init__(self, *args, bitcoin_utility, **kwargs):
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
        try:
            obj = self._try_get(validated_data, blocks=blocks.id)
        except self.Meta.model.DoesNotExist:
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

    def to_schedule(self):
        return pd.DataFrame(self.data['data'])

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
            'blocks', 'model', 'initial', 'mean', 'volatility', 'data'
        )
        list_serializer_class = ProjectListSerializer
        validators = []  # Removes the "unique together" constraint.

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
            'blocks', 'model', 'initial', 'mean', 'volatility', 'data'
        )
        list_serializer_class = ProjectListSerializer
        validators = []  # Removes the "unique together" constraint.

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
            'blocks', 'model', 'initial', 'mean', 'volatility', 'data'
        )
        list_serializer_class = ProjectListSerializer
        validators = []  # Removes the "unique together" constraint.