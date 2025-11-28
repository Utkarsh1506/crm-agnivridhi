"""
Django settings for agnivridhi_crm project.

Agnivridhi India - Complete CRM System
Production-ready configuration with environment variables
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-w=1cy8to$#w_@okqkg)^x3c%q=4^5xnnju2br(lmuhe&)q)kq_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',  # Swagger/OpenAPI documentation
    
    # Local apps
    'accounts',
    'clients',
    'bookings',
    'applications',
    'schemes',
    'edit_requests',
    'payments',
    'documents',
    'notifications',
    'activity_logs',
    'tracking',
    'invoices',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files in production
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom role-based access control MUST run after AuthenticationMiddleware
    'accounts.middleware.RoleAccessMiddleware',
    # Custom idle timeout middleware MUST run after AuthenticationMiddleware
    'accounts.middleware.SessionIdleTimeoutMiddleware',
]

ROOT_URLCONF = 'agnivridhi_crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'applications.context_processors.pending_applications_count',
                'accounts.context_processors.dashboard_link',
            ],
        },
    },
]

WSGI_APPLICATION = 'agnivridhi_crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Support both SQLite (development) and MySQL (production)
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.mysql':
    # MySQL Configuration for Production (Hostinger)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }
else:
    # SQLite Configuration for Development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Static root for collectstatic command (production)
STATIC_ROOT = os.getenv('STATIC_ROOT', BASE_DIR / 'staticfiles')

# Media uploads (user files like payment proofs)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', BASE_DIR / 'media')

# Enable WhiteNoise for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' if not DEBUG else 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
CLIENT_LOGIN_URL = os.getenv('CLIENT_LOGIN_URL', 'https://agnivridhicrm.pythonanywhere.com/login/')


# Email Configuration (Hostinger SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@agnivridhiindia.com'
EMAIL_HOST_PASSWORD = 'NoReply@121'
DEFAULT_FROM_EMAIL = 'Agnivridhi CRM <noreply@agnivridhiindia.com>'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# drf-spectacular (Swagger/OpenAPI) Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'Agnivridhi CRM API',
    'DESCRIPTION': 'Complete CRM API for Agnivridhi India - Manage clients, bookings, payments, and applications',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/',
    'CONTACT': {
        'name': 'Agnivridhi India',
        'email': 'admin@agnivridhiindia.com',
    },
    'LICENSE': {
        'name': 'Proprietary',
    },
}

# WhatsApp Configuration (Twilio)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')  # Twilio Sandbox

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# -----------------------------------------------------------------------------
# Session and security settings (production-ready defaults configurable via .env)
# -----------------------------------------------------------------------------
# NOTE: For local development you may keep these relaxed. In production set the
# environment variables to secure values (SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True,
# SECURE_SSL_REDIRECT=True, etc.) behind HTTPS.

# Use secure cookies for session and CSRF when running over HTTPS
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'

# Make session cookie inaccessible to JavaScript
SESSION_COOKIE_HTTPONLY = True

# Session lifetime (seconds). Default: 1 day (86400). Adjust as needed.
SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', '86400'))

# Whether session expires when browser is closed. Default: False (keep persistent session)
SESSION_EXPIRE_AT_BROWSER_CLOSE = os.getenv('SESSION_EXPIRE_AT_BROWSER_CLOSE', 'False') == 'True'

# Idle timeout: automatically logout after X seconds of inactivity. Set to 0 to disable.
SESSION_IDLE_TIMEOUT = int(os.getenv('SESSION_IDLE_TIMEOUT', '1800'))  # 30 minutes default

# HTTP Strict Transport Security (HSTS) - enable in production when using HTTPS
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False') == 'True'
SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD', 'False') == 'True'

# Redirect all non-HTTPS requests to HTTPS if enabled in env
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'

# If sitting behind a proxy (e.g. nginx) set this header to respect X-Forwarded-Proto
USE_X_FORWARDED_HOST = os.getenv('USE_X_FORWARDED_HOST', 'False') == 'True'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if os.getenv('SECURE_PROXY_SSL_HEADER', 'False') == 'True' else None


# Custom error handlers
# These allow custom branded error pages with user context
handler403 = 'accounts.views.custom_403_view'
handler404 = 'accounts.views.custom_404_view'
handler500 = 'accounts.views.custom_500_view'

# File Upload Settings
# Maximum file upload size: 1MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1048576  # 1MB in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 1048576  # 1MB in bytes

