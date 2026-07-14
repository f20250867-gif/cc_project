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

### 2. Create Virtual Environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your own values:
```bash
cp .env.example .env
```

### 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
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

cc_project/
│
├── cc_project/                     # main project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                          # authentication & user management
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── logout.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── teams/                          # teams, membership, roles, invitations
│   ├── migrations/
│   ├── templates/
│   │   └── teams/
│   │       ├── base.html
│   │       ├── team_form.html
│   │       ├── team_detail.html
│   │       ├── team_members.html
│   │       ├── invite_member.html
│   │       ├── assign_role.html
│   │       └── join_requests.html
│   ├── static/
│   │   └── teams/
│   │       └── main.css
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── mixins.py                   # UserAccessMixin etc.
│   ├── models.py                   # Team, TeamMembership, JoinRequest
│   ├── signals.py
│   ├── urls.py
│   ├── utils.py                    # is_team_owner, is_team_maintainer, etc.
│   └── views.py
│
├── projects/                       # project management
│   ├── migrations/
│   ├── templates/
│   │   └── projects/
│   │       ├── project_form.html
│   │       ├── project_detail.html
│   │       └── project_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Project
│   ├── urls.py
│   └── views.py
│
├── tasks/                          # task management, assignment
│   ├── migrations/
│   ├── templates/
│   │   └── tasks/
│   │       ├── task_form.html
│   │       ├── task_detail.html
│   │       ├── task_assign.html
│   │       └── task_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Task
│   ├── urls.py
│   └── views.py
│
├── comments/                       # commenting system
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Comment
│   ├── urls.py
│   └── views.py
│
├── activity/                       # activity log (cross-cutting)
│   ├── migrations/
│   ├── templates/
│   │   └── activity/
│   │       └── activity_list.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── mixins.py                   # ActivityLogMixin
│   ├── models.py                   # Activity
│   └── urls.py
│
├── templates/                      # project-level shared templates (optional)
│   └── 403.html
│
├── static/                         # project-level static (optional, collected)
│
├── .env                            # NOT committed (in .gitignore)
├── .env.example                    # committed - template for required env vars
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md
└── ENGINEERING_DECISIONS.md

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


  
  
      
      
    
      
