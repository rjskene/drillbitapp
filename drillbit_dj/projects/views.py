import json
import pandas as pd

from celery.result import AsyncResult
from django.http import HttpResponse
from django.db.models import ProtectedError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend, filterset
from rest_framework import filters


from .models import RigForProject, InfraForProject, Project, Projects, \
    ProjectSimulation, ProjectStatement, ProjectStatementSummary
from .serializers import RigForProjectSerializer, InfraForProjectSerializer, ProjectSerializer, \
    ProjectsSerializer, ProjectScalingSerializer, ProjectCostsSerializer, \
    ProjectSimulationSerializer, ProjectStatementSerializer, \
    ProjectStatementSummarySerializer
from .tasks import create_statements_for_given_project
from environment.models import Environment

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

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        try: 
            project.delete()
        except ProtectedError as e:
            sims = ProjectSimulation.objects.filter(project=project)
            ProjectStatement.objects.filter(sim__in=sims).delete()
            ProjectStatementSummary.objects.filter(sim__in=sims).delete()
            sims.delete()
            project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
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

    @action(detail=False, methods=['delete'], name='Delete all statements')
    def delete_all_statements(self, request, *args, **kwargs):
        sim_ids = request.data
        sims = ProjectSimulation.objects.filter(id__in=sim_ids)
        ProjectStatement.objects.filter(sim__in=sims).delete()
        ProjectStatementSummary.objects.filter(sim__in=sims).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectStatementViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectStatementSerializer
    queryset = ProjectStatement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'sim': ['in', 'exact'], # note the 'in' field
        'frequency': ['in', 'exact']
    }

    def create(self, request, *args, **kwargs):
        """
        Custom create that supports creation of statements for multiple simulations

        Create accepts a list of simulation ids, for each of which it creates a pre-defined 
        set of financial statements.

        This creation thus has two dimensions:
            1. the number of simulations
            2. the various frequencies for each simulation
            
        The parameter structure is as follows:
            + if request.data is not a list, make it a list
            + from the list of simulation ids, a new data structure is created that 
            contains the simulation id and the frequency, so that serializer can validate the data

        The base block-level statement is created for each simulation along with the 
        summary statement, inside the serializer. The remaining statements for 
        periods ['H', 'D', 'M', 'Q', 'A'] are create asynchronously via celery tasks.

        The method returns a dictionary of the task ids for each simulation so the status can be 
        monitored by the client separately.

        Parameters
        ----------
        request : rest_framework.request.Request
            The request object that contains a list of simulation ids in the request.data attribute.
            If request.data is not a list, it is converted to a list.

        Return
        --------
        A dictionary of simulation ids and the tasks that were created for each simulation
        """
        
        if not isinstance(request.data, list):
            request.data = [request.data]

        data = []
        for d in request.data:
            data.append({
                'sim': d,
                'frequency': '10T'
            })
        
        serializer = self.get_serializer(data=data, many=isinstance(data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        tasks = {}
        for sim_id in request.data:
            sim_tasks = create_statements_for_given_project(sim_id)
            tasks[sim_id] = sim_tasks

        return Response(
            tasks,
            status=status.HTTP_201_CREATED, 
        )

    @action(detail=False, methods=['get'], name='Check Statement Exists')
    def exists(self, request, *args, **kwargs):
        environment = request.query_params.get('environment', None)
        projects = request.GET.getlist('projects[]', None)
        frequency = request.query_params.get('frequency', 'M')
        
        try:
            environment = Environment.objects.get(pk=environment)
        except Environment.DoesNotExist:
            return Response(False)

        proj_objs = Project.objects.filter(pk__in=projects)
        if proj_objs.count() != len(projects):
            return Response(False)

        sims = ProjectSimulation.objects.filter(environment=environment, project__in=proj_objs)
        if sims.count() != len(projects):
            return Response(False)

        stats = ProjectStatement.objects.filter(sim__in=sims, frequency=frequency)
        if stats.count() != len(projects):
            return Response(False)

        return Response(True)

    @action(detail=False, methods=['get'], name='Project Statement Accounts')
    def projects_by_account(self, request, *args, **kwargs):
        environment = request.query_params.get('environment', None) 
        projects = request.GET.getlist('projects[]', None)
        frequency = request.query_params.get('frequency', 'M')

        projects = Project.objects.filter(pk__in=projects)
        project_dfs = []
        for project in projects:
            sim = ProjectSimulation.objects.get(environment=environment, project=project.id)
            data = {
                'sim': sim.id,
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
                pd.DataFrame(istat['stat']).set_index('index'),
                pd.DataFrame(roi['stat']).set_index('index') if roi else None,
            )).fillna(0)
            project_dfs.append(df)

        df = pd.concat(
            project_dfs,
            keys=list(projects.values_list('name', flat=True)),
            names=['Project', 'Account']
        ) \
        .reorder_levels([1,0]) \
        .sort_index()

        df.columns = pd.to_datetime(df.columns)
        df = df.T.sort_index().T
        df.columns = df.columns.strftime('%Y-%m')

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

        return Response(df.fillna(0).reset_index().to_dict(orient='records'))

class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()    

def get_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data))

# class InListFilter(df.Filter):
#     """
#     Expects a comma separated list
#     filters values in list
#     """
#     def filter(self, qs, value):
#         if value:
#             return qs.filter(**{self.name+'__in': value.split(',')})
#         return qs

# class MyFilterSet(df.FilterSet):
#     status = InListFilter(name='status')

