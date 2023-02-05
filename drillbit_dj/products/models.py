from django.db import models
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
    pue = models.FloatField('Power Usage Effectiveness')
    price = models.FloatField('Price')

class Cooling(AbstractBaseInfrastructure):
    pass

class HeatRejection(AbstractBaseInfrastructure):
    pass

class Electrical(AbstractBaseInfrastructure):
    pass
