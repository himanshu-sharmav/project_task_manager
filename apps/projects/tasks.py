from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Task
import logging

logger = logging.getLogger(__name__)

@shared_task
def mark_overdue_tasks():
    """Mark overdue tasks and send notifications"""
    overdue_tasks = []
    
    for task in Task.objects.filter(is_active=True, status__in=['todo', 'in_progress']):
        if task.is_overdue:
            overdue_tasks.append(task)
    
    if overdue_tasks:
        logger.info(f"Found {len(overdue_tasks)} overdue tasks")
        
        # Send notifications to assigned users
        for task in overdue_tasks:
            if task.assigned_to and task.assigned_to.email:
                send_overdue_notification.delay(task.id)
    
    return f"Processed {len(overdue_tasks)} overdue tasks"

@shared_task
def send_overdue_notification(task_id):
    """Send overdue task notification"""
    try:
        task = Task.objects.get(id=task_id)
        if task.assigned_to and task.assigned_to.email:
            subject = f'Overdue Task: {task.title}'
            message = f"""
            Hi {task.assigned_to.first_name or task.assigned_to.username},

            The following task is overdue:

            Task: {task.title}
            Project: {task.project.name}
            Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M')}
            Priority: {task.get_priority_display()}

            Please update the task status or contact your project manager.

            Best regards,
            Project Management Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [task.assigned_to.email],
                fail_silently=False,
            )
            logger.info(f"Overdue notification sent for task {task.id}")
    except Task.DoesNotExist:
        logger.error(f"Task {task_id} not found for overdue notification")
    except Exception as e:
        logger.error(f"Failed to send overdue notification: {str(e)}")

@shared_task
def send_daily_summary():
    """Send daily task summary to users"""
    from django.contrib.auth.models import User
    
    for user in User.objects.filter(is_active=True, email__isnull=False):
        user_tasks = Task.objects.filter(assigned_to=user, is_active=True)
        overdue_count = len([t for t in user_tasks if t.is_overdue])
        due_today_count = user_tasks.filter(
            due_date__date=timezone.now().date()
        ).count()
        
        if overdue_count > 0 or due_today_count > 0:
            subject = 'Daily Task Summary'
            message = f"""
            Hi {user.first_name or user.username},

            Your daily task summary:
            - Overdue tasks: {overdue_count}
            - Tasks due today: {due_today_count}
            - Total active tasks: {user_tasks.count()}

            Please check your dashboard for details.

            Best regards,
            Project Management Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
