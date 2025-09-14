from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.projects.models import Project, DevelopmentTask, DesignTask

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            created_by=self.user
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), 'Test Project')

    def test_project_is_not_overdue(self):
        self.assertFalse(self.project.is_overdue)

    def test_progress_percentage_no_tasks(self):
        self.assertEqual(self.project.progress_percentage, 0)

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.project = Project.objects.create(
            name='Test Project',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            created_by=self.user
        )

    def test_development_task_creation(self):
        task = DevelopmentTask.objects.create(
            title='Dev Task',
            project=self.project,
            due_date=timezone.now() + timedelta(days=7),
            technology='python',
            created_by=self.user
        )
        self.assertEqual(task.task_type, 'development')
        self.assertEqual(task.technology, 'python')

    def test_design_task_creation(self):
        task = DesignTask.objects.create(
            title='Design Task',
            project=self.project,
            due_date=timezone.now() + timedelta(days=7),
            design_type='ui_ux',
            created_by=self.user
        )
        self.assertEqual(task.task_type, 'design')
        self.assertEqual(task.design_type, 'ui_ux')
