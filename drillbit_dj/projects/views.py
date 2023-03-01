import pandas as pd
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import RigForProject, InfraForProject, Project, Projects, \
    ProjectSimulation, ProjectStatement, ProjectStatementSummary
from .serializers import RigForProjectSerializer, InfraForProjectSerializer, ProjectSerializer, \
    ProjectsSerializer, ProjectScalingSerializer, ProjectCostsSerializer, \
    ProjectSimulationSerializer, ProjectStatementSerializer, \
    ProjectStatementSummarySerializer
from .tasks import create_statements_for_given_project

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

    # def retrieve(self, request, *args, **kwargs):
    #     frequency = request.query_params.get('frequency', 'M')
    #     stat = self.get_object()
    #     serializer = ProjectStatementSerializer(stat, frequency=frequency)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # custom create that allows many=True
        # frequency is required by the serializer but should NOT
        # be provided in the request.  ONLY '10T' is allowed.
        # All others are created via celery task
        # then you have to take frequency OUT again 
        # for the tasks
        data = request.data.copy()
        if isinstance(data, list):
            for d in data:
                d['frequency'] = '10T'
        else:
            data['frequency'] = '10T'
        
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        tasks = []
        if isinstance(data, list):
            for d in data:
                d.pop('frequency')
                task = create_statements_for_given_project(**d) # DONT NEED TO DELAY THIS NESTED TASK!
                tasks.append(task)
        else:
            data.pop('frequency')
            task = create_statements_for_given_project(**data)
            tasks.append(task)

        headers = self.get_success_headers(serializer.data)
        return Response(
            tasks,
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

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
            ser = ProjectStatementSerializer(data=data)
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

class ProjectStatementSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectStatementSummarySerializer
    queryset = ProjectStatementSummary.objects.all()

    def custom_get_object(self, environment, project):
        sim = ProjectSimulation.objects.get(environment=environment, project=project)
        return ProjectStatementSummary.objects.get(sim=sim)

    def list(self, request, *args, **kwargs):
        environment = request.query_params.get('environment', None)    
        projects = request.GET.getlist('projects[]', None)

        projects = Project.objects.filter(pk__in=projects)
        summs = []
        for project in projects:
            stat = self.custom_get_object(environment, project)
            ser = ProjectStatementSummarySerializer(stat)
            summs.append(ser.data['summary'])

        df = pd.DataFrame(summs).T
        df.columns = [p.name for p in projects]

        return Response(df.reset_index().to_dict(orient='records'))

class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()


from django.http import HttpResponse
from celery.result import AsyncResult
import json

def get_progress(request, task_id):
    print (request, task_id)

    result = AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data))