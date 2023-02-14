from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from drillbit_dj.project import ProjectModel
from products.models import Rig

class RigForProject(ProjectModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='rigs')
    rig = models.ForeignKey(Rig, on_delete=models.PROTECT)
    quantity = models.FloatField('Quantity', null=True)

class InfraForProject(ProjectModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='infrastructure')
    quantity = models.FloatField('Quantity', null=True)

    infra_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    infra_object_id = models.IntegerField()
    infrastructure = GenericForeignKey(
        'infra_content_type',
        'infra_object_id',
    )

class Project(ProjectModel):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    capacity = models.FloatField('Capacity')
    target_ambient_temp = models.FloatField('Target Ambient Temperature', default=95)
    target_overclocking = models.FloatField('Target Overclock Factor', default=1)
    energy_price = models.FloatField('Energy Price')

    def add_rig(self, rig, quantity=None, *args, **kwargs):
        return RigForProject.objects.create(
            project=self,
            rig=rig,
            quantity=quantity,
        )

    def add_infra(self, 
        infra:models.Model=None,
        infra_content_type:ContentType=None,
        infra_object_id:int=None, 
        quantity=None,
        *args,
        **kwargs
        ):
        if infra is None:
            if infra_content_type is None or infra_object_id is None:
                raise ValueError((
                    'If `infra` object is not provided,'
                    'you must provide `infra_content_type` and'
                    'infra_object_id'
                ))
        else:
            infra_content_type = ContentType.objects.get_for_model(infra)
            infra_object_id = infra.pk

        return InfraForProject.objects.create(
            project=self,
            infra_content_type=infra_content_type,
            infra_object_id=infra_object_id,
            quantity=quantity,
        )

class Projects(ProjectModel):
    name = models.CharField('Name', max_length=100)
    projects = models.ManyToManyField(Project)

