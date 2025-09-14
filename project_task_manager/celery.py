import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_task_manager.settings')

app = Celery('project_task_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'mark-overdue-tasks': {
        'task': 'apps.projects.tasks.mark_overdue_tasks',
        'schedule': 60.0,  # Run every 60 seconds
    },
}
