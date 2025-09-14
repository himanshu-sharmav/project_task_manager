from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Project, Task, DevelopmentTask, DesignTask

class TaskInline(admin.TabularInline):
    """Inline editing for tasks"""
    model = Task
    extra = 0
    fields = ['title', 'status', 'priority', 'assigned_to', 'due_date']
    readonly_fields = ['created_at']
    
class DevelopmentTaskInline(admin.TabularInline):
    """Inline editing for development tasks"""
    model = DevelopmentTask
    extra = 0
    fields = ['title', 'status', 'priority', 'assigned_to', 'due_date', 'technology']

class DesignTaskInline(admin.TabularInline):
    """Inline editing for design tasks"""
    model = DesignTask
    extra = 0
    fields = ['title', 'status', 'priority', 'assigned_to', 'due_date', 'design_type']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Enhanced Project Admin"""
    list_display = [
        'name', 'status', 'start_date', 'end_date', 
        'progress_display', 'task_count', 'overdue_status'
    ]
    list_filter = ['status', 'start_date', 'created_at', 'assigned_to']
    search_fields = ['name', 'description']
    date_hierarchy = 'start_date'
    filter_horizontal = ['assigned_to']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'status')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Assignment', {
            'fields': ('assigned_to',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [TaskInline]
    
    actions = ['mark_completed', 'mark_on_hold', 'mark_in_progress']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(task_count=Count('tasks'))
    
    def task_count(self, obj):
        return obj.task_count
    task_count.admin_order_field = 'task_count'
    task_count.short_description = 'Tasks'
    
    def progress_display(self, obj):
        progress = obj.progress_percentage
        color = 'green' if progress >= 80 else 'orange' if progress >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, progress
        )
    progress_display.short_description = 'Progress'
    
    def overdue_status(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Overdue</span>')
        return format_html('<span style="color: green;">On Time</span>')
    overdue_status.short_description = 'Status'
    
    def mark_completed(self, request, queryset):
        queryset.update(status=Project.StatusChoices.COMPLETED)
        self.message_user(request, f"{queryset.count()} projects marked as completed.")
    mark_completed.short_description = "Mark selected projects as completed"
    
    def mark_on_hold(self, request, queryset):
        queryset.update(status=Project.StatusChoices.ON_HOLD)
        self.message_user(request, f"{queryset.count()} projects marked as on hold.")
    mark_on_hold.short_description = "Mark selected projects as on hold"
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status=Project.StatusChoices.IN_PROGRESS)
        self.message_user(request, f"{queryset.count()} projects marked as in progress.")
    mark_in_progress.short_description = "Mark selected projects as in progress"

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Base Task Admin"""
    list_display = [
        'title', 'project', 'status', 'priority', 
        'assigned_to', 'due_date', 'overdue_status'
    ]
    list_filter = ['status', 'priority', 'project', 'assigned_to', 'created_at']
    search_fields = ['title', 'description', 'project__name']
    date_hierarchy = 'due_date'
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'project')
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status', 'priority')
        }),
        ('Timeline & Effort', {
            'fields': ('due_date', 'estimated_hours', 'actual_hours')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_completed', 'mark_in_progress', 'mark_blocked']
    
    def overdue_status(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Overdue</span>')
        return format_html('<span style="color: green;">On Time</span>')
    overdue_status.short_description = 'Status'
    
    def mark_completed(self, request, queryset):
        queryset.update(status=Task.StatusChoices.COMPLETED)
        self.message_user(request, f"{queryset.count()} tasks marked as completed.")
    mark_completed.short_description = "Mark selected tasks as completed"
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status=Task.StatusChoices.IN_PROGRESS)
        self.message_user(request, f"{queryset.count()} tasks marked as in progress.")
    mark_in_progress.short_description = "Mark selected tasks as in progress"
    
    def mark_blocked(self, request, queryset):
        queryset.update(status=Task.StatusChoices.BLOCKED)
        self.message_user(request, f"{queryset.count()} tasks marked as blocked.")
    mark_blocked.short_description = "Mark selected tasks as blocked"

@admin.register(DevelopmentTask)
class DevelopmentTaskAdmin(TaskAdmin):
    """Development Task Admin"""
    list_display = TaskAdmin.list_display + ['technology']
    list_filter = TaskAdmin.list_filter + ['technology']
    search_fields = TaskAdmin.search_fields + ['technology', 'repository_url']
    
    fieldsets = TaskAdmin.fieldsets + (
        ('Development Specific', {
            'fields': ('technology', 'repository_url', 'branch_name', 'pull_request_url')
        }),
    )

@admin.register(DesignTask)
class DesignTaskAdmin(TaskAdmin):
    """Design Task Admin"""
    list_display = TaskAdmin.list_display + ['design_type']
    list_filter = TaskAdmin.list_filter + ['design_type']
    search_fields = TaskAdmin.search_fields + ['design_type', 'design_tool']
    
    fieldsets = TaskAdmin.fieldsets + (
        ('Design Specific', {
            'fields': ('design_type', 'design_tool', 'design_file_url', 'feedback_notes')
        }),
    )

# Admin site customization
admin.site.site_header = "Project Task Management"
admin.site.site_title = "PTM Admin"
admin.site.index_title = "Welcome to Project Task Management Administration"
