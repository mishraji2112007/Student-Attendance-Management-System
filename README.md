# Student Attendance Management System - College Mini Project

Django + SQLite project with Admin, Teacher and Student roles.

Features: student/teacher/subject CRUD, teacher attendance marking, reports, student self-attendance and percentage, Django admin.

## Setup
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations attendance
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Open http://127.0.0.1:8000/

Demo: admin/Admin@123, teacher1/Teacher@123, student1/Student@123
