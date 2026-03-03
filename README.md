# Coderr Backend API

Django REST Framework backend for a marketplace platform (Developer Akademie project).

---

## 🌍 Live Deployment (Render)

Base URL:


https://coderr-backend-1ons.onrender.com/api/


Example endpoint:


GET https://coderr-backend-1ons.onrender.com/api/base-info/


---

## 🔐 Demo Login Credentials

### Business User

username: kevin
password: asdasd24


### Customer User

username: andrey
password: asdasd12


Login endpoint:


POST /api/login/


Example login request:


POST https://coderr-backend-1ons.onrender.com/api/login/


Request Body:

```json
{
  "username": "kevin",
  "password": "asdasd24"
}
🧪 How to Test

You can test the API using:

Django REST Framework browsable API

Postman / Insomnia

A frontend application

Run tests locally:

pytest --cov

Test coverage is above 95%.

🔄 Recreate Demo Users (if needed)

If demo users are missing (e.g. after Render restart):

POST https://coderr-backend-1ons.onrender.com/api/registration/

Business example:

{
  "username": "kevin",
  "password": "asdasd24",
  "type": "business"
}

Customer example:

{
  "username": "andrey",
  "password": "asdasd12",
  "type": "customer"
}
⚙️ Tech Stack

Python

Django

Django REST Framework

django-filter

pytest

pytest-django

pytest-cov

Gunicorn

WhiteNoise

🛠 Local Installation

Clone repository:

git clone https://github.com/mya63/coderr_backend.git
cd coderr_backend

Create virtual environment:

python -m venv venv

Activate environment:

Windows:

venv\Scripts\activate

Mac / Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Start server:

python manage.py runserver

Backend will run at:

http://127.0.0.1:8000/api/
📁 Project Structure

auth_app

profiles_app

offers_app

orders_app

reviews_app

core (base-info endpoint)

All endpoints follow REST principles and use proper permission handling.

🗄 Database

The deployed version uses SQLite.

For production environments, PostgreSQL is recommended.

## 👤 Author

Muhammed Yunus Amini
GitHub: https://github.com/mya63  
Developer Akademie – Fullstack Program (2025–2026)