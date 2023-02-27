import pandas as pd
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import RigForProject, InfraForProject, Project, Projects, \
    ProjectSimulation, ProjectStatement
from .serializers import RigForProjectSerializer, InfraForProjectSerializer, ProjectSerializer, \
    ProjectsSerializer, ProjectScalingSerializer, ProjectCostsSerializer, \
    ProjectSimulationSerializer, ProjectStatementSerializer

class RigForProjectViewSet(viewsets.ModelViewSet):
    serializer_class = RigForProjectSerializer
    queryset = RigForProject.objects.all()

class InfraForProjectViewSet(viewsets.ModelViewSet):
    serializer_class = InfraForProjectSerializer
    queryset = InfraForProject.objects.all()

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def update(self, request, *args, **kwargs):
        # want to return updated data; the original serializer will not do that     
        super().update(request, *args, **kwargs)
        updated_instance = self.get_object()
        updated_serializer = self.get_serializer(updated_instance)
        return Response(updated_serializer.data)

    @action(detail=True, methods=['put'], name='Scale Project')
    def scale(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = ProjectScalingSerializer(project)
        serializer.scale()

        updated_instance = self.get_object()
        updated_serializer = self.get_serializer(updated_instance)
        return Response(updated_serializer.data)

    @action(detail=True, methods=['get'], name='Get Project Costs')
    def costs(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = ProjectCostsSerializer(project)
        return Response(serializer.data['product'])

class ProjectSimulationViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSimulationSerializer
    queryset = ProjectSimulation.objects.all()
        
    def create(self, request, *args, **kwargs):
        # custom create that allows many=True
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProjectStatementViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectStatementSerializer
    queryset = ProjectStatement.objects.all()

    def retrieve(self, request, *args, **kwargs):
        frequency = request.query_params.get('frequency', 'M')
        stat = self.get_object()
        serializer = ProjectStatementSerializer(stat, frequency=frequency)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # custom create that allows many=True
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], name='Project Statement Accounts')
    def projects_by_account(self, request, *args, **kwargs):
        environment = request.query_params.get('environment', None)    
        projects = request.GET.getlist('projects[]', None)
        frequency = request.query_params.get('frequency', 'M')

        projects = Project.objects.filter(pk__in=projects)
        project_dfs = []
        for project in projects:
            data = {
                'environment': environment, 
                'project': project.id, 
                'frequency': frequency
            }
            ser = ProjectStatementSerializer(data=data, frequency=frequency)
            ser.is_valid()
            ser.save()
            env = ser.data['env']
            roi = ser.data['roi']
            istat = ser.data['istat']
            df = pd.concat((
                pd.DataFrame(env['stat']).set_index('index'),
                pd.DataFrame(roi['stat']).set_index('index'),
                pd.DataFrame(istat['stat']).set_index('index'),
            )).fillna(0)
            project_dfs.append(df)

        df = pd.concat(
            project_dfs,
            keys=list(projects.values_list('name', flat=True)),
            names=['Project', 'Account']
        ) \
        .reorder_levels([1,0]) \
        .sort_index()

        response = {
            'labels': df.columns,
            'datasets': {}
        }

        for account, name in df.index:
            if account not in response['datasets']:
                response['datasets'][account] = []
            
            dataset = {
                'label': name,
                'data': df.loc[(account, name)].values.tolist()
            }
            response['datasets'][account].append(dataset)

        return Response(response)

    @action(detail=False, methods=['get'], name='Summary Comparison')
    def summary(self, request, *args, **kwargs):
        environment = request.query_params.get('environment', None)    
        projects = request.GET.getlist('projects[]', None)

        projects = Project.objects.filter(pk__in=projects)
        profs = []
        for project in projects:
            data = {
                'environment': environment, 
                'project': project.id, 
                'frequency': 'M'
            }
            ser = ProjectStatementSerializer(data=data, frequency='M')
            ser.is_valid()
            ser.save()
            profs.append(ser.data['profitability'])

        df = pd.DataFrame(profs).T
        df.columns = [p.name for p in projects]

        return Response(df.reset_index().to_dict(orient='records'))

    @action(detail=True, methods=['get'], name='Get Income Statement')
    def income_statement(self, request, *args, **kwargs):
        frequency = request.query_params.get('frequency', None)

        stat = self.get_object()
        serializer = ProjectStatementSerializer(stat, frequency=frequency)
        
        data = serializer.data['istat']
        
        return Response(serializer.data['istat'])

    @action(detail=True, methods=['get'], name='Get ROI Analysis')
    def roi(self, request, *args, **kwargs):
        frequency = request.query_params.get('frequency', None)
        stat = self.get_object()
        serializer = ProjectStatementSerializer(stat, frequency=frequency)
        return Response(serializer.data['roi'])

    @action(detail=True, methods=['get'], name='Get ROI Analysis')
    def profitability(self, request, *args, **kwargs):
        frequency = request.query_params.get('frequency', None)
        stat = self.get_object()
        serializer = ProjectStatementSerializer(stat, frequency=frequency)
        return Response(serializer.data['profitability'])

class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
