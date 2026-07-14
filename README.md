# CC Project

This Django web application tracks projects and tasks for users within a team.

## Prerequisites

1. Python 3.14.2
2. Django 6.0.2
3. SQLite (default, comes with Python)
4. pip
5. Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/f20250867-gif/cc_project.git
cd cc_project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a Superuser
```bash
python manage.py createsuperuser
```

## Running Locally
```bash
python manage.py runserver
```

Visit in browser:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Repository Structure
```
cc_project/
│
├── cc_project/                     # main project config
│   ├── init.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                          # authentication & user management
│   ├── migrations/
│   ├── templates/users/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── teams/                          # teams, membership, roles, invitations
│   ├── migrations/
│   ├── templates/teams/
│   ├── static/teams/
│   ├── mixins.py
│   ├── models.py                   # Team, TeamMembership, JoinRequest
│   ├── utils.py
│   ├── urls.py
│   └── views.py
│
├── projects/                       # project management
│   ├── migrations/
│   ├── templates/projects/
│   ├── models.py                   # Project
│   ├── urls.py
│   └── views.py
│
├── tasks/                          # task management, assignment
│   ├── migrations/
│   ├── templates/tasks/
│   ├── models.py                   # Task
│   ├── urls.py
│   └── views.py
│
├── comments/                       # commenting system
│   ├── migrations/
│   ├── models.py                   # Comment
│   ├── urls.py
│   └── views.py
│
├── activity/                       # activity log (cross-cutting)
│   ├── migrations/
│   ├── templates/activity/
│   ├── mixins.py                   # ActivityLogMixin
│   ├── models.py                   # Activity
│   └── urls.py
│                               
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md
└── ENGINEERING_DECISIONS.md
```
## Technologies Used

- Python
- Django
- SQLite/PostgreSQL
- HTML/CSS
- JavaScript

## Features

- Team creation with role-based access (Owner, Maintainer, Member, Viewer)
- Project and task management within teams
- Task assignment to multiple users
- Comments on tasks
- Activity log tracking key events
- Join requests and invitations for team membership


  
  
      
      
    
      
