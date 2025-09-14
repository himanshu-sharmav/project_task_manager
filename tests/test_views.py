from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.projects.models import Project

class ProjectAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        data = {
            'name': 'Test Project',
            'description': 'Test Description',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'status': 'planning'
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)

    def test_get_projects(self):
        Project.objects.create(
            name='Test Project',
            start_date='2023-01-01',
            end_date='2023-12-31',
            created_by=self.user
        )
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
