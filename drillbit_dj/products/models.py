from django.db import models
from django.forms.models import model_to_dict

from drillbit.__new_objects import Rig as RigManager, Product as ProductManager, \
    Cooling as CoolingManager, HeatRejection as HeatRejectionManager
from drillbit_dj.project import ProjectModel

class AbstractBaseRig(ProjectModel):
    
    class Meta:
        abstract = True

    make = models.CharField('Make', max_length=100)
    model = models.CharField(max_length=100)
    generation = models.CharField(max_length=100, null=True, blank=True)
    manufacturer = models.CharField(max_length=100)

    hash_rate = models.FloatField()
    power = models.FloatField()
    buffer = models.FloatField() # excess power draw versus spec

    price = models.FloatField(null=True, blank=True, default=0)

    @property
    def name(self):
        name = f'{self.make} {self.model}'

        if self.generation:
            if not self.generation.isalpha() or len(self.generation) == 1:
                name += f'{self.generation}'
            else:
                name += f' {self.generation}'
        
        return name

    @property
    def efficiency(self):
        return self.power / self.hash_rate

    def as_drillbit_object(self):
        kwargs = model_to_dict(self)
        kwargs.pop('id')

        return RigManager(**kwargs)

    def __str__(self):
        return self.name

class Rig(AbstractBaseRig):
    pass
    # class Meta:
    #     # unique together may not apply to ProjectRig
    #     unique_together = ('make', 'model', 'generation')

class AbstractBaseInfrastructure(ProjectModel):
    
    class Meta:
        abstract = True
    
    name = models.CharField('Name', max_length=100)
    power = models.FloatField('Power', default=None)
    pue = models.FloatField('Power Usage Effectiveness')
    price = models.FloatField('Price')

class Cooling(AbstractBaseInfrastructure):
    number_of_rigs = models.FloatField('Number of rigs', default=None, null=True)

    def as_drillbit_object(self):
        kwargs = model_to_dict(self)
        kwargs.pop('id')

        return CoolingManager(**kwargs)

class RejectionCurve(models.Model):
    """
    Slope and intercept of a linear equation that defines
    the heat rejection capacity (in power terms) of a system as a function
    of the ambient temperature.
    """
    a = models.FloatField()
    b = models.FloatField()

class HeatRejection(AbstractBaseInfrastructure):
    curve = models.ForeignKey(RejectionCurve, on_delete=models.PROTECT, default=1)

    def as_drillbit_object(self):
        kwargs = model_to_dict(self)
        kwargs.pop('id')
        curve = RejectionCurve.objects.get(pk=kwargs['curve'])
        kwargs['curve'] = (curve.a, curve.b)

        return HeatRejectionManager(**kwargs)

class Electrical(AbstractBaseInfrastructure):
    def as_drillbit_object(self):
        kwargs = model_to_dict(self)
        kwargs.pop('id')

        return ProductManager(**kwargs)
