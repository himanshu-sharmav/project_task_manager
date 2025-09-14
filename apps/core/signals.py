from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging
import sys

# Import the actual model classes
from apps.projects.models import Task, DevelopmentTask, DesignTask, Project

logger = logging.getLogger(__name__)

@receiver(post_save, sender='projects.DevelopmentTask')  # String reference
@receiver(post_save, sender='projects.DesignTask')       # String reference
@receiver(post_save, sender='projects.Task')            # Use actual model class
def task_created_notification(sender, instance, created, **kwargs):
    """Send notification when a task is created"""
    print(f"🔥 Signal fired! Task: {instance.title}, Created: {created}")
    
    if not created:
        print("❌ Task was updated, not created. No email sent.")
        return
        
    if not (instance.assigned_to and instance.assigned_to.email):
        print("❌ No assigned user or email. No email sent.")
        return
        
    subject = f'New Task Assigned: {instance.title}'
    message = f"""
Hi {instance.assigned_to.first_name or instance.assigned_to.username},

You have been assigned a new task:

Task: {instance.title}
Project: {instance.project.name}
Due Date: {instance.due_date.strftime('%Y-%m-%d %H:%M')}
Priority: {instance.get_priority_display()}

Please log in to view more details.

Best regards,
Project Management Team
"""
    
    try:
        send_mail(
            subject,
            message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
            [instance.assigned_to.email],
            fail_silently=False,
        )
        print(f"✅ Email sent to {instance.assigned_to.email}")
        logger.info(f"Task notification sent to {instance.assigned_to.email}")
    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        logger.error(f"Failed to send task notification: {str(e)}")
        if 'test' in sys.argv:
            raise

@receiver(pre_delete, sender=Project)
def cascade_delete_project_tasks(sender, instance, **kwargs):
    """Log cascade deletion of project tasks"""
    task_count = instance.tasks.count()
    logger.info(f"Project '{instance.name}' deleted. {task_count} tasks will be cascade deleted.")
