from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from apps.projects.models import Project, DevelopmentTask

class SignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass',
            email='test@example.com'
        )
        self.project = Project.objects.create(
            name='Test Project',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            created_by=self.user
        )

    def test_task_creation_sends_email(self):
        # Clear any existing emails
        mail.outbox = []
        
        # Create a task assigned to a user with email
        task = DevelopmentTask.objects.create(
            title='Test Task',
            project=self.project,
            assigned_to=self.user,
            due_date=timezone.now() + timedelta(days=7),
            created_by=self.user
        )
        
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('New Task Assigned', mail.outbox[0].subject)
        self.assertIn(self.user.email, mail.outbox[0].to)
        
    def test_no_email_sent_when_no_assigned_user(self):
        # Clear any existing emails
        mail.outbox = []
        
        # Create a task without assigned user
        task = DevelopmentTask.objects.create(
            title='Test Task',
            project=self.project,
            due_date=timezone.now() + timedelta(days=7),
            created_by=self.user
        )
        
        # Check that no email was sent
        self.assertEqual(len(mail.outbox), 0)
   