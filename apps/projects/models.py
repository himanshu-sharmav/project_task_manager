from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel

class Project(BaseModel):
    """Project model extending BaseModel"""
    
    class StatusChoices(models.TextChoices):
        PLANNING = 'planning', 'Planning'
        IN_PROGRESS = 'in_progress', 'In Progress'
        REVIEW = 'review', 'Review'
        COMPLETED = 'completed', 'Completed'
        ON_HOLD = 'on_hold', 'On Hold'

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.PLANNING
    )
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_to = models.ManyToManyField(
        User, 
        related_name='assigned_projects', 
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError('Start date must be before end date')

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.end_date < timezone.now().date() and self.status != self.StatusChoices.COMPLETED

    @property
    def progress_percentage(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(status='completed').count()
        return round((completed_tasks / total_tasks) * 100, 2)


class Task(BaseModel):
    """Base Task model"""
    
    class StatusChoices(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        REVIEW = 'review', 'Review'
        COMPLETED = 'completed', 'Completed'
        BLOCKED = 'blocked', 'Blocked'

    class PriorityChoices(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks'
    )
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.TODO
    )
    priority = models.CharField(
        max_length=10, 
        choices=PriorityChoices.choices, 
        default=PriorityChoices.MEDIUM
    )
    due_date = models.DateTimeField()
    estimated_hours = models.PositiveIntegerField(default=0)
    actual_hours = models.PositiveIntegerField(default=0, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['due_date']),
            models.Index(fields=['project', 'status']),
        ]

    def __str__(self):
        return f"{self.title} - {self.project.name}"

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date < timezone.now() and self.status != self.StatusChoices.COMPLETED

    @property
    def task_type(self):
        return self.__class__.__name__.replace('Task', '').lower()


class DevelopmentTask(Task):
    """Development specific task"""
    
    class TechnologyChoices(models.TextChoices):
        PYTHON = 'python', 'Python'
        JAVASCRIPT = 'javascript', 'JavaScript'
        JAVA = 'java', 'Java'
        REACT = 'react', 'React'
        DJANGO = 'django', 'Django'
        OTHER = 'other', 'Other'

    technology = models.CharField(
        max_length=20, 
        choices=TechnologyChoices.choices, 
        default=TechnologyChoices.PYTHON
    )
    repository_url = models.URLField(blank=True)
    branch_name = models.CharField(max_length=100, blank=True)
    pull_request_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Development Task"
        verbose_name_plural = "Development Tasks"


class DesignTask(Task):
    """Design specific task"""
    
    class DesignTypeChoices(models.TextChoices):
        UI_UX = 'ui_ux', 'UI/UX Design'
        GRAPHIC = 'graphic', 'Graphic Design'
        WIREFRAME = 'wireframe', 'Wireframe'
        PROTOTYPE = 'prototype', 'Prototype'
        MOCKUP = 'mockup', 'Mockup'

    design_type = models.CharField(
        max_length=20, 
        choices=DesignTypeChoices.choices, 
        default=DesignTypeChoices.UI_UX
    )
    design_tool = models.CharField(max_length=50, blank=True)
    design_file_url = models.URLField(blank=True)
    feedback_notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Design Task"
        verbose_name_plural = "Design Tasks"
