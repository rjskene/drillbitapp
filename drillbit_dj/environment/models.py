import json
import pandas as pd

from django.db import models
from drillbit_dj.project import ProjectModel

class ScheduleModel(ProjectModel):
    class Meta:
        abstract = True

    def to_frame(self):
        return pd.DataFrame(json.loads(self.json))

class BlockSchedule(ScheduleModel):
    start_date = models.DateField()
    last_epoch = models.PositiveSmallIntegerField()
    
    json = models.JSONField()

    class Meta:
        unique_together = ('id', 'start_date', 'last_epoch')

# Django choice field for the environment model
ENVIRONMENT_MODELS = (
    ('Constant', 'Constant'),
    ('CGR', 'CGR'),
    ('GBM', 'GBM'),
)
class EnvironmentSchedule(ScheduleModel):
    class Meta:
        abstract = True
        unique_together = ('initial', 'mean', 'volatility', 'model', 'blocks')

    blocks = models.ForeignKey(BlockSchedule, on_delete=models.PROTECT)
    model = models.CharField(max_length=20, choices=ENVIRONMENT_MODELS)

    initial = models.FloatField()
    mean = models.FloatField(null=True)
    volatility = models.FloatField(null=True)

    json = models.JSONField()

class BitcoinPrice(EnvironmentSchedule):
    pass

class TransactionFees(EnvironmentSchedule):
    pass

class HashRate(EnvironmentSchedule):
    pass