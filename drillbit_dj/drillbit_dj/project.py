import pandas as pd

from django.db import models
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action

### DATABASE ###
class ProjectModelManager(models.Manager):
    def to_frame(self, **filters):
        columns = [f.name for f in self.model._meta.get_fields() if f.concrete and not f.many_to_many] # excludes hidden relation fields ... does it exclude anything else?????
        
        if filters:
            values = self.filter(**filters).values_list()
        else:
            values = self.all().values_list()

        return pd.DataFrame(
            values,
            columns=columns
        )

class ProjectModel(models.Model):
    objects = ProjectModelManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

### Serializers ###
class GetOrCreateSerializerMixin:
    """
    Forecast Model Types use `get_or_create` functionality in the serializer
    """
    def _try_get(self, validated_data, *args, **kwargs):
        obj = self.Meta.model.objects.get(*args, **validated_data, **kwargs)
        self._created = False
        return obj

    def _schedule_create(self, schedule, validated_data, *args, **kwargs):
        json = schedule.to_json(orient='records')
        obj = self.Meta.model.objects.create(*args, json=json, **validated_data, **kwargs)
        self._created = True
        return obj

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if hasattr(self, '_created'):
            repr['__new_object_created__'] = self._created  # This is a hack to get the created status into the response

        return repr

class BulkUpdateSerializerMixin:
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        obj_mapping = {obj.id: obj for obj in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        created = []
        for obj_id, data in data_mapping.items():
            obj = obj_mapping.get(obj_id, None)
            if obj is None:
                ret.append(self.child.create(data))
                created.append(ret[-1].id)
            else:
                ret.append(self.child.update(obj, data))

        # Perform deletions for the current forecast
        to_delete = self.child.Meta.model.objects.exclude(id__in=list(data_mapping.keys())).exclude(id__in=created)
        to_delete.delete()

        return ret

class ProjectListSerializer(BulkUpdateSerializerMixin, serializers.ListSerializer):
    def to_frame(self, convert_to_periods=[], **kwargs):
        df = pd.DataFrame(self.data)
        
        if isinstance(convert_to_periods, str):
            convert_to_periods = [convert_to_periods]
        
        for col in convert_to_periods:
            df.loc[:, col] = pd.PeriodIndex(df[col], freq='D')

        return df

### ViewSets ###
class BulkUpdateViewSetMixin:
    @action(detail=False, methods=['put'], url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        data = request.data.get('data', None)

        if data:
            instances = self.model.objects.filter(pk__in=[d['id'] for d in data if isinstance(d['id'], int)])
            serializer = self.get_serializer(instances, data=data, many=True, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
    
            return Response(serializer.data)
        else:
            return Response({'error': 'No data provided.'})
            