from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from drillbit.__new_objects import RigOperator, CoolingOperator, HeatRejectionOperator, \
    ElectricalOperator, Project as ProjectManager

from drillbit_dj.project import ProjectModel
from products.models import Rig, Cooling, HeatRejection, Electrical, WeatherStation
from environment.models import Environment

class RigForProject(ProjectModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='rigs')
    rig = models.ForeignKey(Rig, on_delete=models.PROTECT)
    quantity = models.FloatField('Quantity', null=True)
    price = models.FloatField('Price', null=True)
    amortization = models.FloatField('Amortization', default=60)

    def as_drillbit_object(self):
        return RigOperator(
            product=self.rig.as_drillbit_object(), 
            quantity=self.quantity, 
            overclocking=self.project.target_overclocking
        )

class InfraForProject(ProjectModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='infrastructure')
    quantity = models.FloatField('Quantity', null=True)
    price = models.FloatField('Price', null=True)
    amortization = models.FloatField('Amortization', default=60)

    infra_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    infra_object_id = models.IntegerField()
    infrastructure = GenericForeignKey(
        'infra_content_type',
        'infra_object_id',
    )

    def as_drillbit_object(self):
        if self.infrastructure is None:
            raise ValueError('`infrastructure` must be set')
        elif isinstance(self.infrastructure, Cooling):
            return CoolingOperator(
                product=self.infrastructure.as_drillbit_object(),
                quantity=self.quantity,
                price=self.price,
            )
        elif isinstance(self.infrastructure, HeatRejection):
            return HeatRejectionOperator(
                product=self.infrastructure.as_drillbit_object(),
                quantity=self.quantity,
                price=self.price,
            )
        elif isinstance(self.infrastructure, Electrical):
            return ElectricalOperator(
                product=self.infrastructure.as_drillbit_object(),
                quantity=self.quantity,
                price=self.price,
            )

class Project(ProjectModel):
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    capacity = models.FloatField('Capacity')

    ambient_temp_source = models.ForeignKey(
        WeatherStation, 
        on_delete=models.PROTECT,
        related_name='projects',
        null=True,
    )
    target_ambient_temp = models.JSONField('Target Ambient Temperature', default=dict, null=True)
    target_overclocking = models.FloatField('Target Overclock Factor', default=1)
    energy_price = models.FloatField('Energy Price')

    pool_fees = models.FloatField('Pool Fees', default=0)
    tax_rate = models.FloatField('Tax Rate', default=0)
    opex = models.FloatField('Opex', default=0)
    property_taxes = models.FloatField('Property Taxes', default=0)

    def add_rig(self, rig, quantity=None, price=None, *args, **kwargs):
        return RigForProject.objects.create(
            project=self,
            rig=rig,
            quantity=quantity,
            price=price,
        )

    def add_infra(self, 
        infra:models.Model=None,
        infra_content_type:ContentType=None,
        infra_object_id:int=None, 
        quantity=None,
        price=None,
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
            price=price,
        )

    def as_drillbit_object(self, target_ambient_temp=None):
        """
        Allow outside target_ambient_temp to be passed in, if the
        target_ambient_temp is being manipulated outside of the model
        """
        target_ambient_temp = target_ambient_temp or self.target_ambient_temp

        return ProjectManager(
            name=self.name,
            capacity=self.capacity,
            target_ambient_temp=target_ambient_temp,
            target_overclocking=self.target_overclocking,
            energy_price=self.energy_price,
            rigs=[rig.as_drillbit_object() for rig in self.rigs.all()][0], # only use first rig for now
            infrastructure=[infra.as_drillbit_object() for infra in self.infrastructure.all()],
        )

class ProjectSimulation(ProjectModel):
    environment = models.ForeignKey(Environment, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

FREQUENCY_CHOICES = (
    ('10T', '10 Minutes'),
    ('D', 'Daily'),
    ('M', 'Monthly'),
    ('Q', 'Quarterly'),
    ('A', 'Annually')
)
class ProjectStatement(ProjectModel):
    sim = models.ForeignKey(ProjectSimulation, on_delete=models.PROTECT)
    frequency = models.CharField('Frequency', max_length=10, choices=FREQUENCY_CHOICES)

    env = models.JSONField(default=dict)
    istat = models.JSONField(default=dict)
    roi = models.JSONField(default=dict)

class ProjectStatementSummary(ProjectModel):
    sim = models.ForeignKey(ProjectSimulation, on_delete=models.PROTECT)
    summary = models.JSONField(default=dict)

class Projects(ProjectModel):
    name = models.CharField('Name', max_length=100)
    projects = models.ManyToManyField(Project)

