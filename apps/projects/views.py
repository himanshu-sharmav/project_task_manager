from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Project, Task, DevelopmentTask, DesignTask
from .serializers import (
    ProjectSerializer, TaskSerializer, 
    DevelopmentTaskSerializer, DesignTaskSerializer
)
from .filters import ProjectFilter, TaskFilter

class ProjectViewSet(viewsets.ModelViewSet):
    """Project ViewSet with CRUD operations"""
    queryset = Project.objects.filter(is_active=True).prefetch_related('assigned_to', 'tasks')
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'name']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue projects"""
        overdue_projects = [p for p in self.get_queryset() if p.is_overdue]
        serializer = self.get_serializer(overdue_projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def tasks_summary(self, request, pk=None):
        """Get task summary for a project"""
        project = self.get_object()
        tasks = project.tasks.all()
        
        summary = {
            'total_tasks': tasks.count(),
            'completed_tasks': tasks.filter(status='completed').count(),
            'in_progress_tasks': tasks.filter(status='in_progress').count(),
            'overdue_tasks': len([t for t in tasks if t.is_overdue]),
            'progress_percentage': project.progress_percentage,
        }
        return Response(summary)

class TaskViewSet(viewsets.ModelViewSet):
    """Base Task ViewSet"""
    queryset = Task.objects.filter(is_active=True).select_related('project', 'assigned_to')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue tasks"""
        overdue_tasks = [t for t in self.get_queryset() if t.is_overdue]
        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get current user's tasks"""
        tasks = self.get_queryset().filter(assigned_to=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

class DevelopmentTaskViewSet(viewsets.ModelViewSet):
    """Development Task ViewSet"""
    queryset = DevelopmentTask.objects.filter(is_active=True).select_related('project', 'assigned_to')
    serializer_class = DevelopmentTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description', 'technology']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class DesignTaskViewSet(viewsets.ModelViewSet):
    """Design Task ViewSet"""
    queryset = DesignTask.objects.filter(is_active=True).select_related('project', 'assigned_to')
    serializer_class = DesignTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description', 'design_type']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
