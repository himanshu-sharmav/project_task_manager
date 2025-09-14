from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Task, DevelopmentTask, DesignTask

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False)
    task_type = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'assigned_to', 
            'assigned_to_id', 'status', 'priority', 'due_date', 
            'estimated_hours', 'actual_hours', 'task_type', 'is_overdue',
            'created_at', 'updated_at'
        ]

class DevelopmentTaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = DevelopmentTask
        fields = [
            'id', 'title', 'description', 'project', 'assigned_to', 
            'assigned_to_id', 'status', 'priority', 'due_date', 
            'estimated_hours', 'actual_hours', 'technology', 
            'repository_url', 'branch_name', 'pull_request_url',
            'is_overdue', 'created_at', 'updated_at'
        ]

class DesignTaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = DesignTask
        fields = [
            'id', 'title', 'description', 'project', 'assigned_to', 
            'assigned_to_id', 'status', 'priority', 'due_date', 
            'estimated_hours', 'actual_hours', 'design_type', 
            'design_tool', 'design_file_url', 'feedback_notes',
            'is_overdue', 'created_at', 'updated_at'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(many=True, read_only=True)
    assigned_to_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True, 
        required=False
    )
    tasks = TaskSerializer(many=True, read_only=True)
    tasks_count = serializers.SerializerMethodField()
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'start_date', 
            'end_date', 'assigned_to', 'assigned_to_ids', 'tasks', 
            'tasks_count', 'progress_percentage', 'is_overdue',
            'created_at', 'updated_at'
        ]
    
    def get_tasks_count(self, obj):
        return obj.tasks.count()
    
    def create(self, validated_data):
        assigned_to_ids = validated_data.pop('assigned_to_ids', [])
        project = Project.objects.create(**validated_data)
        if assigned_to_ids:
            project.assigned_to.set(assigned_to_ids)
        return project
    
    def update(self, instance, validated_data):
        assigned_to_ids = validated_data.pop('assigned_to_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if assigned_to_ids is not None:
            instance.assigned_to.set(assigned_to_ids)
        return instance
