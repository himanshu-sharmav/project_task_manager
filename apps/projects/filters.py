import django_filters
from django import forms
from .models import Project, Task, DevelopmentTask, DesignTask

class ProjectFilter(django_filters.FilterSet):
    """Project filtering"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Project.StatusChoices.choices)
    start_date_after = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_before = django_filters.DateFilter(field_name='start_date', lookup_expr='lte')
    end_date_after = django_filters.DateFilter(field_name='end_date', lookup_expr='gte')
    end_date_before = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    assigned_to = django_filters.NumberFilter(field_name='assigned_to__id')

    class Meta:
        model = Project
        fields = ['name', 'status', 'start_date_after', 'start_date_before', 
                 'end_date_after', 'end_date_before', 'assigned_to']

class TaskFilter(django_filters.FilterSet):
    """Task filtering"""
    title = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Task.StatusChoices.choices)
    priority = django_filters.ChoiceFilter(choices=Task.PriorityChoices.choices)
    project = django_filters.NumberFilter(field_name='project__id')
    assigned_to = django_filters.NumberFilter(field_name='assigned_to__id')
    due_date_after = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='gte')
    due_date_before = django_filters.DateTimeFilter(field_name='due_date', lookup_expr='lte')
    
    class Meta:
        model = Task
        fields = ['title', 'status', 'priority', 'project', 'assigned_to', 
                 'due_date_after', 'due_date_before']
