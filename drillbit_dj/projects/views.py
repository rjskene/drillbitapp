from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import RigForProject, InfraForProject, Project, Projects
from .serializers import RigForProjectSerializer, InfraForProjectSerializer, ProjectSerializer, \
    ProjectsSerializer, ProjectScalingSerializer, ProjectCostsSerializer

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

class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
