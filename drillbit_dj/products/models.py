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
    capacity = models.FloatField('Power Capacity', default=None, null=True)
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
    a = models.FloatField(null=True)
    b = models.FloatField(null=True)
    r = models.FloatField(null=True)
    p = models.FloatField(null=True)
    serr = models.FloatField(null=True)

    raw = models.JSONField(default=dict)

    def r_squared(self):
        return self.r ** 2

class HeatRejection(AbstractBaseInfrastructure):
    curve = models.ForeignKey(RejectionCurve, on_delete=models.SET_DEFAULT, default=None, null=True)
    design_dry_bulb = models.FloatField('Design Dry Bulb Temperature', default=95, null=True)

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

class WeatherStation(ProjectModel):
    id = models.CharField('ID', primary_key=True, max_length=6)
    
    location = models.CharField('Location', max_length=100)
    region = models.CharField('Region', max_length=100)
    
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')
    elevation = models.FloatField('Elevation (in feet))')

    def __str__(self):
        return self.location

class WeatherData(ProjectModel):
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE)

    type = models.CharField(max_length=100)
    units = models.CharField(max_length=100, null=True, default='IP')
    period = models.CharField(max_length=100, null=True)
    variable = models.CharField(max_length=100)

    data = models.JSONField(default=dict)

# Algorithm for quickly modelling heat rejection curves
# for sheet in p_sheets:
#     rej = HeatRejection.objects.get(design_dry_bulb=int(sheet))
    
#     raw = xl.parse(sheet).loc[:, ['Ambient Temp (F)', 'Capacity (kW)']].dropna()
#     raw = raw.rename(columns={'Capacity (kW)': 'Capacity (W)'})
#     raw.loc[:, 'Capacity (W)'] = raw['Capacity (W)'] * 1000
#     raw = raw \
#         .set_index('Ambient Temp (F)') \
#         .loc[int(sheet):] \
#         .reset_index()

#     curve, _ = RejectionCurve.objects.get_or_create(raw=raw.to_dict('list'))
#     rej.curve = curve
#     rej.save()

# for curve in RejectionCurve.objects.all():
#     x, y = np.array(list(curve.raw.values()))
    
#     curve.a, curve.b, curve.r, curve.p, curve.serr = scist.linregress(x, y)
#     curve.save()

# fname = 'weather_station_details.csv'
# df = pd.read_csv(fpath + fname)

# def f(value):
#     if 'E' in value or 'N' in value:
#         return float(value[:-1])
#     elif 'W' in value or 'S' in value:
#         return -float(value[:-1])
#     else:
#         raise
        
# df.Latitude = df.Latitude.apply(f)
# df.Longitude = df.Longitude.apply(f)
# df.columns = df.columns.str.lower()
# df.location = df.location.str.title()
# df.elevation = df.elevation.str.replace('ft', '').astype(int)

# WeatherStation.objects.bulk_create(WeatherStation(**row.to_dict()) for idx, row in df.iterrows())

# fpath = '/Users/spindicate/Documents/programming/weather-stations/dry_bulb_frequency_by_location/'

# datas = []
# for fname in tqdm(os.listdir(fpath)):
#     if not '.DS_Store' in fname:
#         df = pd.read_csv(fpath + fname, skiprows=8)
#         data = WeatherData(
#             station=WeatherStation.objects.get(id=fname.split('_')[0]),
#             data=df.to_dict('list'),
#             type='single-variable frequency',
#             units='IP',
#             period='annual',
#             variable='Dry-Bulb'
#         )
#         datas.append(data)