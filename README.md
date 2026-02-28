# Coderr Backend API

This project is a Django REST Framework backend for a marketplace platform.

It includes:

- Authentication (Registration + Login)
- User Profiles (Customer / Business roles)
- Offers with multiple OfferDetails
- Orders with status workflow
- Reviews with rating system
- Aggregated base information endpoint

---

## 🌍 Live Deployment

Backend is deployed on Render:

Base URL:
https://coderr-backend-1ons.onrender.com/api/

Example endpoint:
https://coderr-backend-1ons.onrender.com/api/base-info/

---

## 🔐 Demo Login Credentials

Business User:
username: kevin  
password: asdasd24  

Customer User:
username: andrey  
password: asdasd12  

Login endpoint:
POST /api/login/

---

## 🧪 How to Test

You can test the API in multiple ways:

1. Use the Django REST Framework browsable API in the browser
2. Use Postman / Insomnia
3. Connect a frontend application

Example login request:

POST https://coderr-backend-1ons.onrender.com/api/login/

Body:
{
  "username": "kevin",
  "password": "asdasd24"
}

---

## ⚙️ Tech Stack

- Python
- Django
- Django REST Framework
- django-filter
- pytest
- pytest-django
- pytest-cov

---

## 🛠 Installation (Local Development)

Clone the repository:

```bash
git clone <your-repo-url>
cd coderr_backend


Create and activate virtual environment:

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Start development server:

python manage.py runserver
✅ Run Tests
pytest --cov

Test coverage is above 95%.

📁 Project Structure

auth_app

profiles_app

offers_app

orders_app

reviews_app

core (base-info endpoint)

All endpoints are protected with proper permission handling and follow REST principles.

🗄 Database

The deployed version currently uses SQLite.
For production environments, PostgreSQL is recommended.