from pathlib import Path
import os

# Define base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================
# Security & Environment Config
# ==============================

# Load SECRET_KEY from environment (fallback only for local development)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# DEBUG controlled via environment variable (1 = True, 0 = False)
DEBUG = os.environ.get("DEBUG", "0") == "1"

# Required for correct HTTPS handling on Render (reverse proxy setup)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# Enforce secure cookies in production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

# Render-specific hostname (used for dynamic configuration)
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

# Allowed hosts for local + Render deployment
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]

# Add Render hostname dynamically if available
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# ==============================
# Installed Applications
# ==============================

INSTALLED_APPS = [
    "corsheaders",  # Enable CORS handling for frontend communication

    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    "rest_framework",               # Django REST Framework
    "rest_framework.authtoken",     # Token-based authentication
    "django_filters",               # Filtering support for query parameters

    # Local project apps
    "auth_app",
    "profiles_app",
    "offers_app",
    "orders_app",
    "reviews_app",
]


# ==============================
# Middleware Configuration
# ==============================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Handle CORS before CommonMiddleware

    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# ==============================
# Database Configuration
# ==============================

# SQLite database (sufficient for development and small deployments)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================
# Password Validation
# ==============================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================
# Internationalization
# ==============================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# ==============================
# Static Files Configuration
# ==============================

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Use WhiteNoise for compressed static files in production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ==============================
# Django REST Framework Settings
# ==============================

REST_FRAMEWORK = {
    # Use token authentication globally
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],

    # All endpoints require authentication by default
    # Public endpoints explicitly override this
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    # Enable django-filter for query parameter filtering
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}


# ==============================
# CORS & CSRF Configuration
# ==============================

# Allow local frontend development server
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

CORS_ALLOW_CREDENTIALS = True

# Trust local frontend for CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

# Add Render domain to CSRF trusted origins if deployed
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")