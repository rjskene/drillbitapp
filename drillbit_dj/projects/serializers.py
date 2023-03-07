import json
import pandas as pd

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers

from drillbit.__new_objects import Project as ProjectManager
from drillbit.statements.statements import init_environment, ProjectTemplate, ROITemplate, \
    analysis

from drillbit_dj.project import ProjectListSerializer, GetOrCreateSerializerMixin

from .models import RigForProject, InfraForProject, Project, Projects, \
    ProjectSimulation, ProjectStatement, ProjectStatementSummary

from environment.models import Environment
from environment.serializers import BlockScheduleSerializer, BitcoinPriceSerializer, \
    TransactionFeesSerializer, HashRateSerializer, BitcoinUtilityInitMixin
from products.models import Rig, Cooling, HeatRejection, Electrical, RejectionCurve
from products.serializers import RigSerializer, CoolingSerializer, HeatRejectionSerializer, ElectricalSerializer

class StatementFromJSONConversionField(serializers.JSONField):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, value):
        value = json.loads(value)
        value = pd.DataFrame(value)            
        stat = {
            'stat': value.reset_index().to_dict(orient='records'),
            'columns': value.reset_index().columns.tolist()
        }
        return stat

class RigForProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    rig = RigSerializer(read_only=True)
    rig_id = serializers.PrimaryKeyRelatedField(queryset=Rig.objects.all())

    class Meta:
        model = RigForProject
        fields = (
            'id', 
            'project',
            'quantity',
            'amortization',
            'rig', 
            'rig_id'
        )
        list_serializer_class = ProjectListSerializer

class InfrastructureRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `infrastructure` generic relationship.
    """
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Cooling):
            return CoolingSerializer(value).data
        elif isinstance(value, HeatRejection):
            return HeatRejectionSerializer(value).data
        elif isinstance(value, Electrical):
            return ElectricalSerializer(value).data
        else:
            raise Exception('Unknown infrastructure type')

class InfraForProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    infrastructure = InfrastructureRelatedField(read_only=True)
    infra_content_type = serializers.SlugRelatedField(queryset=ContentType.objects.all(), slug_field='model')
    infra_object_id = serializers.IntegerField()

    class Meta:
        model = InfraForProject
        fields = (
            'id', 
            'project',
            'quantity',
            'amortization',
            'infrastructure',
            'infra_content_type', 
            'infra_object_id',
        )
        list_serializer_class = ProjectListSerializer

class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) # needs to be declared explicilty so it is not read-only and available for updates
    rigs = RigForProjectSerializer(many=True, required=False)
    infrastructure = InfraForProjectSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = (
            'id',
            'name', 'description',
            'capacity', 
            'energy_price',
            'target_ambient_temp',
            'target_overclocking',
            'pool_fees',
            'tax_rate',
            'opex',
            'property_taxes',
            'rigs', 
            'infrastructure'
        )
        list_serializer_class = ProjectListSerializer

    def create(self, validated_data):
        rigs_data = validated_data.pop('rigs', [])
        infrastructure_data = validated_data.pop('infrastructure', [])
        project = Project.objects.create(**validated_data)
        
        for rig_data in rigs_data:
            rig_data['rig'] = rig_data.pop('rig_id')
            project.add_rig(**rig_data)

        for infra_data in infrastructure_data:
            project.add_infra(**infra_data)

        return project

    def update(self, project, validated_data):
        rigs_data = validated_data.pop('rigs', [])
        infra_data = validated_data.pop('infrastructure', [])

        project._meta.model.objects \
            .filter(pk=project.pk) \
            .update(**validated_data)

        # delete rigs and infra that are not in the list
        RigForProject.objects \
            .filter(project=project) \
            .exclude(id__in=[rig_data['id'] for rig_data in rigs_data if 'id' in rig_data]) \
            .delete()

        for rig_data in rigs_data:
            if 'id' not in rig_data:
                rig_data['rig'] = rig_data.pop('rig_id')
                project.add_rig(**rig_data)
            else:
                pk = rig_data.pop('id')
                rig_data['rig'] = rig_data.pop('rig_id')
                RigForProject.objects \
                    .filter(pk=pk) \
                    .update(**rig_data)

        # delete infra that are not in the list
        InfraForProject.objects \
            .filter(project=project) \
            .exclude(id__in=[infra_data['id'] for infra_data in infra_data if 'id' in infra_data]) \
            .delete()
        
        for infra_data in infra_data:
            if 'id' not in infra_data:
                project.add_infra(**infra_data)
            else:
                InfraForProject.objects \
                    .filter(id=infra_data['id']) \
                    .update(**infra_data)

        return project

class ProjectsSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    project_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Project.objects.all(), 
        write_only=True
    )

    class Meta:
        model = Projects
        fields = ('id', 'name', 'projects', 'project_ids')

    def create(self, validated_data):
        project_ids = validated_data.pop('project_ids', [])
        projects = Projects.objects.create(**validated_data)
        
        for project_id in project_ids:
            projects.projects.add(project_id)

        return projects

    def update(self, projects, validated_data):
        project_ids = validated_data.pop('project_ids', [])

        projects._meta.model.objects \
            .filter(pk=projects.pk) \
            .update(**validated_data)

        for project_id in project_ids:
            projects.projects.add(project_id)

        return projects

class DrillbitRelatedField(serializers.RelatedField):
    """
    Returns the corresponding `drillbit` package object of a model instance
    """
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        return value.as_drillbit_object()

class RigForProjectScalingSerializer(serializers.ModelSerializer):
    rig = DrillbitRelatedField(read_only=True)

    class Meta:
        model = RigForProject
        fields = (
            'id', 
            'quantity',
            'rig', 
        )
        list_serializer_class = ProjectListSerializer

class InfraForProjectScalingSerializer(serializers.ModelSerializer):
    infrastructure = DrillbitRelatedField(read_only=True)

    class Meta:
        model = InfraForProject
        fields = (
            'quantity',
            'infrastructure',
        )
        list_serializer_class = ProjectListSerializer

class ProjectScalingSerializer(serializers.ModelSerializer):
    rigs = RigForProjectScalingSerializer(many=True, required=False)
    infrastructure = InfraForProjectScalingSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = (
            'capacity', 
            'energy_price',
            'target_ambient_temp',
            'target_overclocking',
            'rigs', 'infrastructure'
        )
        list_serializer_class = ProjectListSerializer

    def to_representation(self, instance):
        value = super().to_representation(instance)
        value['rigs'] = [rig['rig'] for rig in value['rigs']]
        value['infrastructure'] = [infra['infrastructure'] for infra in value['infrastructure']]
        return value

    def scale(self):
        proj = ProjectManager(**self.data)
        proj.scale()

        rig = self.instance.rigs.all()[0]
        rig.quantity = proj.rigs.quantity
        rig.save()

        for (infra, scaled) in zip(self.instance.infrastructure.all(), proj.infrastructure ):
            infra.quantity = scaled.quantity
            infra.save()

class RigCostsForProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='rig.name', read_only=True)
    price = serializers.FloatField(source='rig.price', read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = RigForProject
        fields = (
            'name',
            'price',
            'quantity',
            'total_cost',
        )
        list_serializer_class = ProjectListSerializer

    def get_total_cost(self, obj):
        return obj.quantity * obj.rig.price

class InfraCostsForProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='infrastructure.name', read_only=True)
    price = serializers.FloatField(source='infrastructure.price', read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = InfraForProject
        fields = (
            'name',
            'price',
            'quantity',
            'total_cost',
        )
        list_serializer_class = ProjectListSerializer

    def get_total_cost(self, obj):
        return obj.quantity * obj.infrastructure.price

class ProductCostsRelatedField(serializers.RelatedField):
    """
    Returns the corresponding `drillbit` package object of a model instance
    """
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        return value

class ProjectCostsSerializer(serializers.ModelSerializer):
    rigs = RigCostsForProjectSerializer(many=True, read_only=True)
    infrastructure = InfraCostsForProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'rigs',
            'infrastructure',
            # 'total_cost',
        )
        list_serializer_class = ProjectListSerializer

    def to_representation(self, instance):
        """
        Reduces the data structure to a list of products
        
        Returns:
        restuctured_data (dict): A dictionary with a single key `product`
            -> if restructured_data is a list, the serializer raises an exception

        """
        data = super().to_representation(instance)
        restructured_data = {}
        restructured_data['product'] = []
        for k, product_group in data.items():
            for product in product_group:
                product['product'] = k
                restructured_data['product'].append(product)
        
        print (restructured_data)

        return restructured_data

class ProjectSimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSimulation
        fields = '__all__'
        list_serializer_class = ProjectListSerializer

    def create(self, validated_data):
        obj, created = ProjectSimulation.objects.get_or_create(**validated_data)
        return obj

class ProjectStatementSerializer(
    BitcoinUtilityInitMixin,
    serializers.ModelSerializer
):
    environment = serializers.PrimaryKeyRelatedField(
        source='sim.environment',
        queryset=Environment.objects.all(),
    )
    project = serializers.PrimaryKeyRelatedField(
        source='sim.project',
        queryset=Project.objects.all()
    )
    name = serializers.CharField(source='sim.project.name', read_only=True)

    env = StatementFromJSONConversionField(read_only=True)
    istat = StatementFromJSONConversionField(read_only=True)
    roi = StatementFromJSONConversionField(read_only=True)

    class Meta:
        model = ProjectStatement
        fields = (
            'id',
            'name',
            'project',
            'environment',
            'env',
            'istat',
            'roi',
            'frequency'
        )

    def create(self, validated_data):
        data = validated_data.copy()
        sim, created = ProjectSimulation.objects.get_or_create(**data['sim'])
        frequency = data.pop('frequency')
        try:
            obj = ProjectStatement.objects.get(sim=sim, frequency=frequency)
        except ProjectStatement.DoesNotExist:
            if frequency == '10T':
                env, istat, roi, summary = create_new_block_level_statement(sim)
            else:
                try: 
                    obj = ProjectStatement.objects.get(sim=sim, frequency='10T')
                except ProjectStatement.DoesNotExist:
                    raise serializers.ValidationError((
                        'You must save the block level '
                        'statements first.'
                    ))
                env = load_json_block_statement_and_resample(obj.env, frequency)
                istat = load_json_block_statement_and_resample(obj.istat, frequency)
                roi = load_json_block_statement_and_resample(obj.roi, frequency)

            with transaction.atomic():
                obj = ProjectStatement.objects.create(
                    sim=sim,
                    frequency=frequency,
                    env=env,
                    istat=istat,
                    roi=roi,
                )
                if frequency == '10T':
                    summ = ProjectStatementSummary.objects.create(
                        sim=sim,
                        summary=summary,
                    )

        return obj

def create_new_block_level_statement(sim):
    blocks = BlockScheduleSerializer(
        sim.environment.block_schedule, 
    ).to_schedule(with_period_index=True)
    price = BitcoinPriceSerializer(
        sim.environment.bitcoin_price, 
    ).to_schedule()
    fees = TransactionFeesSerializer(
        sim.environment.transaction_fees,
    ).to_schedule()
    hash_rate = HashRateSerializer(
        sim.environment.hash_rate, 
    ).to_schedule()

    env = init_environment(
        blocks,
        price.forecast,
        fees.forecast,
        hash_rate.forecast * 1e6 * 1e12 # convert from M TH/s to H/s
    )
    project = sim.project.as_drillbit_object()
    stat = ProjectTemplate(env, project)

    env = stat.env.to_frame(with_periods=False).to_json()
    istat = stat.istat.to_frame(with_periods=False).to_json()
    roi = stat.roi.to_frame(with_periods=False).to_json()
    summary = analysis(stat, project).summary()

    return env, istat, roi, summary

def load_json_block_statement_and_resample(value, frequency):
    value = json.loads(value)
    df = pd.DataFrame(value)

    # have to catch different formats between ROI and others
    if len(df.columns[0]) == 7:
        fmt = '%Y-%m'
    else:
        fmt = '%d-%m-%y %H:%M'

    df.columns = pd.to_datetime(df.columns, format=fmt)
    # HERE I NEED DIFFERENT RESAMPLE FUNCTIONS FOR DIFFERENT
    # ROWS .....!!!!!
    last = [
        'Number of Rigs',   
    ]
    mean = [
        'Hash Rate', # technically INCORRECT; should add up all hashes in period, divide by seconds in period
        'Hash Share',
    ]
    aggs = {}
    for index in df.index:
        if index in last:
            aggs[index] = 'last'
        elif index in mean:
            aggs[index] = 'mean'
        else:
            aggs[index] = 'sum'

    df = df.T.resample(frequency).agg(aggs).T
    df.columns = df.columns.strftime('%Y-%m-%d')
    
    return df.to_json()

class ProjectStatementSummarySerializer(serializers.ModelSerializer):
    environment = serializers.PrimaryKeyRelatedField(
        source='sim.environment',
        queryset=Environment.objects.all()
    )
    project = serializers.PrimaryKeyRelatedField(
        source='sim.project',
        queryset=Project.objects.all()
    )
    summary = serializers.JSONField(read_only=True)

    class Meta:
        model = ProjectStatementSummary
        fields = (
            'environment',
            'project',
            'summary',
        )
        list_serializer_class = ProjectListSerializer

    def create(self, *args, **kwargs):
        raise NotImplementedError('Create not allowed on this serializer')
