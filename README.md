## 🚀 Live Test

Test the application directly in the browser:

👉 https://mya63.github.io/coderr_frontend/

Guest login is available – no registration required.


# Coderr Backend API

Django REST Framework backend for a marketplace platform.  
This project was developed as part of the Developer Akademie.

---

# 🌍 Live Deployment

Base URL

```

[https://coderr-backend-1ons.onrender.com/api/](https://coderr-backend-1ons.onrender.com/api/)

```

Example endpoint

```

GET /api/base-info/

```

Full example

```

[https://coderr-backend-1ons.onrender.com/api/base-info/](https://coderr-backend-1ons.onrender.com/api/base-info/)

```

---

# 🔐 Demo Login

### Business user

```

username: kevin
password: asdasd24

```

### Customer user

```

username: andrey
password: asdasd12

```

Login endpoint

```

POST /api/login/

````

Example request

```json
{
  "username": "kevin",
  "password": "asdasd24"
}
````

---

# 🧪 Running Tests

Run tests locally

```
pytest
```

---

# ⚙️ Local Installation

Clone repository

```
git clone https://github.com/mya63/coderr_backend.git
```

Enter project folder

```
cd coderr_backend
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

---

# 🔧 Environment Variables

Create a `.env` file based on `.env.example`

```
SECRET_KEY=your-secret-key
DEBUG=1
```

---

# 📦 Install Dependencies

```
pip install -r requirements.txt
```

---

# 🗄 Run Migrations

```
python manage.py migrate
```

---

# 🚀 Start Development Server

```
python manage.py runserver
```

Local API base

```
http://127.0.0.1:8000/api/
```

---

# 🧱 Tech Stack

* Python
* Django
* Django REST Framework
* django-filter
* pytest
* Gunicorn
* WhiteNoise

---

# 👨‍💻 Author

Muhammed Yunus Amini

```

---

