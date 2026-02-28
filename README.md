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

## Tech Stack

- Python
- Django
- Django REST Framework
- django-filter
- pytest
- pytest-django
- pytest-cov

---

## Installation

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
Run Tests
pytest --cov

Test coverage is above 95%.

API Base URL
http://127.0.0.1:8000/api/
Project Structure

auth_app

profiles_app

offers_app

orders_app

reviews_app

core (base-info endpoint)

All endpoints are protected with proper permission handling and follow REST principles.