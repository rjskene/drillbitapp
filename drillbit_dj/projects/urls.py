from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('rig', views.RigForProjectViewSet, basename='rig') 
router.register('infrastructure', views.InfraForProjectViewSet, basename='infrastructure')
router.register('project', views.ProjectViewSet, basename='project')
router.register('simulation', views.ProjectSimulationViewSet, basename='simulation')
router.register('statement', views.ProjectStatementViewSet, basename='project-statement')
router.register('summary', views.ProjectStatementSummaryViewSet, basename='project-statement-summary')
router.register('projects', views.ProjectsViewSet, basename='projects')

urlpatterns = [
    path('tasks/<str:task_id>', views.get_progress, name='task-status')
]

urlpatterns += router.urls