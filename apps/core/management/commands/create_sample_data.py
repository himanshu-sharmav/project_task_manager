from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.projects.models import Project, DevelopmentTask, DesignTask

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create users
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'first_name': f'User{i}',
                    'last_name': 'Test',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        # Create projects
        projects = []
        project_data = [
            {'name': 'E-commerce Platform', 'description': 'Build a complete e-commerce solution'},
            {'name': 'Mobile App Development', 'description': 'Develop mobile app for iOS and Android'},
            {'name': 'Website Redesign', 'description': 'Redesign company website'},
        ]
        
        for data in project_data:
            project, created = Project.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'status': 'in_progress',
                    'start_date': timezone.now().date(),
                    'end_date': timezone.now().date() + timedelta(days=90),
                    'created_by': users[0]
                }
            )
            project.assigned_to.set(users[:3])
            projects.append(project)
        
        # Create development tasks
        dev_tasks_data = [
            {'title': 'Setup Django Project', 'technology': 'django'},
            {'title': 'Create User Authentication', 'technology': 'python'},
            {'title': 'Build Product Catalog', 'technology': 'django'},
            {'title': 'Implement Payment Gateway', 'technology': 'python'},
        ]
        
        for i, data in enumerate(dev_tasks_data):
            DevelopmentTask.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': f'Description for {data["title"]}',
                    'project': projects[i % len(projects)],
                    'assigned_to': users[i % len(users)],
                    'status': 'in_progress' if i % 2 == 0 else 'todo',
                    'priority': 'high' if i % 3 == 0 else 'medium',
                    'due_date': timezone.now() + timedelta(days=7 + i),
                    'estimated_hours': 8 + i * 2,
                    'technology': data['technology'],
                    'created_by': users[0]
                }
            )
        
        # Create design tasks
        design_tasks_data = [
            {'title': 'Design Landing Page', 'design_type': 'ui_ux'},
            {'title': 'Create Logo Design', 'design_type': 'graphic'},
            {'title': 'Build Wireframes', 'design_type': 'wireframe'},
            {'title': 'Design Mobile Mockups', 'design_type': 'mockup'},
        ]
        
        for i, data in enumerate(design_tasks_data):
            DesignTask.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': f'Description for {data["title"]}',
                    'project': projects[i % len(projects)],
                    'assigned_to': users[i % len(users)],
                    'status': 'review' if i % 2 == 0 else 'in_progress',
                    'priority': 'urgent' if i % 4 == 0 else 'medium',
                    'due_date': timezone.now() + timedelta(days=5 + i),
                    'estimated_hours': 6 + i * 3,
                    'design_type': data['design_type'],
                    'design_tool': 'Figma' if i % 2 == 0 else 'Adobe XD',
                    'created_by': users[0]
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
