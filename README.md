# Coderr Backend API

Django REST Framework backend for a marketplace platform.  
This project was developed as part of the Developer Akademie.

---

# 🌍 Live Deployment

Base URL

```
https://coderr-backend-1ons.onrender.com/api/
```

Example endpoint

```bash
GET /api/base-info/
```

Full example

```
https://coderr-backend-1ons.onrender.com/api/base-info/
```

---

# 🔐 Demo Login

## Business user

```
username: kevin
password: asdasd24
```

## Customer user

```
username: andrey
password: asdasd12
```

Login endpoint

```bash
POST /api/login/
```

Example request

```json
{
  "username": "kevin",
  "password": "asdasd24"
}
```

---

# 🧪 Running Tests

Run tests locally with pytest

```bash
pytest
```

---

# ⚙️ Local Installation

Clone repository

```bash
git clone https://github.com/mya63/coderr_backend.git
```

Go into project folder

```bash
cd coderr_backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Start development server

```bash
python manage.py runserver
```

Local API base

```
http://127.0.0.1:8000/api/
```

---

# 🧱 Tech Stack

- Python  
- Django  
- Django REST Framework  
- django-filter  
- pytest  
- Gunicorn  
- WhiteNoise  

---

# 👨‍💻 Author

Muhammed Yunus Amini 