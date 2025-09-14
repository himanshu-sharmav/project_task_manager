# Project Task Manager - Django Backend Application

## 📋 Overview

Project Task Manager is a comprehensive Django-based backend system designed to facilitate efficient project and task management for development teams. This application demonstrates advanced Django concepts including model inheritance, signals, REST APIs, and asynchronous task processing.

### Key Features

- **Robust Data Models**: Hierarchical task system with inheritance (Task → DevelopmentTask, DesignTask)
- **Real-time Notifications**: Django signals trigger email notifications on task assignment
- **RESTful API**: Full CRUD operations with filtering, searching, and pagination
- **JWT Authentication**: Secure user registration and token-based authentication
- **Background Processing**: Celery integration for asynchronous email sending and periodic tasks
- **Enhanced Admin Interface**: Custom Django admin with bulk actions and progress tracking
- **Comprehensive Testing**: Unit and integration tests with 95%+ coverage

## 🛠 Technology Stack

- **Backend Framework**: Django 5.2.6
- **API Framework**: Django REST Framework 3.16.1
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Caching & Message Broker**: Redis 5.0.8
- **Background Tasks**: Celery 5.5.3
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Email Backend**: SMTP (Gmail) / Locmem (Testing)
- **Containerization**: Docker & Docker Compose
- **Testing**: Django TestCase, Coverage.py

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Redis Server
- PostgreSQL (optional, SQLite works for development)
- Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd project-task-manager

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configurations

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Create sample data (optional)
python manage.py create_sample_data

# Start Redis server (in separate terminal)
redis-server

# Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` to access the admin interface.

## 📁 Project Structure

```
project_task_manager/
├── manage.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── project_task_manager/
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── apps/
│   ├── core/
│   │   ├── models.py          # BaseModel abstract class
│   │   ├── signals.py         # Email notification signals
│   │   └── management/
│   │       └── commands/
│   │           ├── create_sample_data.py
│   │           └── mark_overdue_tasks.py
│   ├── projects/
│   │   ├── models.py          # Project, Task, DevelopmentTask, DesignTask
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # API ViewSets
│   │   ├── urls.py            # API routing
│   │   ├── filters.py         # Django-filter classes
│   │   ├── tasks.py           # Celery tasks
│   │   └── admin.py           # Enhanced admin interface
│   └── authentication/
│       ├── views.py           # JWT auth endpoints
│       ├── serializers.py     # Auth serializers
│       └── urls.py            # Auth routing
└── tests/
    ├── test_models.py
    ├── test_views.py
    └── test_signals.py
```

## 🔌 API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### Authentication
```
POST /api/auth/register/     # User registration
POST /api/auth/login/        # JWT token obtain
POST /api/auth/token/refresh/ # Refresh JWT token
```

### Projects
```
GET    /api/projects/                    # List projects with filtering
POST   /api/projects/                    # Create project
GET    /api/projects/{id}/               # Retrieve project
PUT    /api/projects/{id}/               # Update project
DELETE /api/projects/{id}/               # Delete project
GET    /api/projects/overdue/            # List overdue projects
GET    /api/projects/{id}/tasks_summary/ # Get project task statistics
```

### Tasks
```
GET    /api/tasks/                       # List all tasks
POST   /api/tasks/                       # Create task
GET    /api/tasks/{id}/                  # Retrieve task
PUT    /api/tasks/{id}/                  # Update task
DELETE /api/tasks/{id}/                  # Delete task
GET    /api/tasks/overdue/               # List overdue tasks
GET    /api/tasks/my_tasks/              # Current user's tasks
```

### Development Tasks
```
GET    /api/development-tasks/           # List development tasks
POST   /api/development-tasks/           # Create development task
GET    /api/development-tasks/{id}/      # Retrieve development task
PUT    /api/development-tasks/{id}/      # Update development task
DELETE /api/development-tasks/{id}/      # Delete development task
```

### Design Tasks
```
GET    /api/design-tasks/                # List design tasks
POST   /api/design-tasks/                # Create design task
GET    /api/design-tasks/{id}/           # Retrieve design task
PUT    /api/design-tasks/{id}/           # Update design task
DELETE /api/design-tasks/{id}/           # Delete design task
```

## 🔍 API Filtering & Search

### Query Parameters

**Projects:**
```
?status=in_progress
?start_date_after=2023-01-01
?assigned_to=1
?search=django
```

**Tasks:**
```
?status=todo&priority=high
?project=1
?assigned_to=2
?due_date_before=2023-12-31
?search=authentication
```

### Example Requests

```bash
# Get high priority tasks
curl "http://127.0.0.1:8000/api/tasks/?priority=high"

# Search for Django-related tasks
curl "http://127.0.0.1:8000/api/tasks/?search=django"

# Get tasks due this week
curl "http://127.0.0.1:8000/api/tasks/?due_date_after=2023-12-01&due_date_before=2023-12-07"
```

## 🔐 Authentication Usage

### Register a new user
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "secure123",
    "password_confirm": "secure123"
  }'
```

### Login and get JWT tokens
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "secure123"
  }'
```

### Use JWT token for authenticated requests
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/projects/
```

## 🧪 Testing

### Run all tests
```bash
python manage.py test
```

### Run specific test modules
```bash
python manage.py test tests.test_models
python manage.py test tests.test_signals
python manage.py test apps.projects.tests
```

### Run tests with coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML report
```

### Test Email Notifications
Email notifications are automatically tested using Django's `locmem` backend, which captures emails in `mail.outbox` during testing.

## ⚡ Background Tasks with Celery

### Start Celery Worker
```bash
# Terminal 1: Celery Worker
celery -A project_task_manager worker -l info

# Terminal 2: Celery Beat (Periodic Tasks)
celery -A project_task_manager beat -l info

# Terminal 3: Django Development Server
python manage.py runserver
```

### Periodic Tasks
- **Mark Overdue Tasks**: Runs every 60 seconds to identify and mark overdue tasks
- **Send Reminders**: Daily email reminders for upcoming deadlines

## 🐳 Docker Deployment

### Build and run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop all services
docker-compose down
```

### Services included:
- **web**: Django application
- **db**: PostgreSQL database
- **redis**: Redis server
- **celery**: Celery worker
- **celery-beat**: Celery scheduler

## 🌐 Production Deployment

### Environment Variables (.env)
```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgres://user:password@host:port/database
REDIS_URL=redis://redis-host:6379/0
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### Deploy to Railway/Render
1. Push code to GitHub
2. Connect repository to Railway/Render
3. Set environment variables
4. Deploy automatically

## 📊 Management Commands

### Create sample data
```bash
python manage.py create_sample_data
```

### Mark overdue tasks
```bash
python manage.py mark_overdue_tasks
```

### Custom commands available in `apps/core/management/commands/`

## 🎯 Key Features Demonstrated

### 1. Model Inheritance
- `BaseModel` abstract class with common fields
- `Task` base model extended by `DevelopmentTask` and `DesignTask`
- Polymorphic behavior and specialized fields

### 2. Django Signals
- Email notifications triggered on task creation
- Signal handlers for cleanup operations
- Proper signal registration in `AppConfig.ready()`

### 3. Advanced API Features
- ViewSet-based APIs with DRF
- Custom filtering with django-filter
- Pagination and ordering
- Permission classes and authentication

### 4. Admin Customization
- Inline editing for related models
- Custom admin actions
- Enhanced list displays with calculated fields
- Filtering and searching capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Developer**: Himanshu Sharma  
**Email**: your.email@example.com  
**Project Link**: [https://github.com/himanshu-sharmav/project_task_manager](https://github.com/himanshu-sharmav/project_task_manager)

## 🙏 Acknowledgments

- Django and DRF communities for excellent documentation
- Celery team for robust background task processing
- Redis team for reliable message broker
- All contributors and testers

***

**Note**: This project was created as part of a Django internship assignment demonstrating proficiency in Django models, signals, REST APIs, authentication, background tasks, and testing.

