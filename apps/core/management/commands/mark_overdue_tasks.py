from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.projects.models import Task

class Command(BaseCommand):
    help = 'Mark overdue tasks and send notifications'

    def handle(self, *args, **options):
        overdue_tasks = []
        current_time = timezone.now()
        
        for task in Task.objects.filter(is_active=True):
            if task.is_overdue:
                overdue_tasks.append(task)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Found {len(overdue_tasks)} overdue tasks at {current_time}'
            )
        )
        
        for task in overdue_tasks:
            self.stdout.write(
                f'- {task.title} (Due: {task.due_date}, Project: {task.project.name})'
            )
