from pathlib import Path
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
import os
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# SEGURIDAD
# ===============================

SECRET_KEY = os.environ.get('SECRET_KEY')

# En desarrollo siempre True
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    'www.cedhu.edu.co',
    'cedhu.edu.co',
    'website-cedhu.onrender.com',
    '127.0.0.1',
    'localhost'
]

CSRF_TRUSTED_ORIGINS = [
    'https://website-cedhu-production.up.railway.app',
    'https://www.cedhu.edu.co',
    'https://cedhu.edu.co',
]

# ===============================
# APLICACIONES
# ===============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_browser_reload',
    'core',
    'plataforma',
    'padres',
    'estudiantes',
]

# ===============================
# MIDDLEWARE
# ===============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise solo necesario en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ===============================
# TEMPLATES
# ===============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # opcional si usas carpeta global
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ===============================
# BASE DE DATOS
# ===============================

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Usa URL (desarrollo / staging / producción)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600
        )
    }
else:
    # Usa configuración local (pgAdmin)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# ===============================
# VALIDADORES
# ===============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===============================
# INTERNACIONALIZACIÓN
# ===============================

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===============================
# ARCHIVOS ESTÁTICOS
# ===============================

STATIC_URL = '/static/'

# En desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static',
]

# En producción
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ===============================
# MEDIA
# ===============================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===============================
# LOGIN
# ===============================

LOGIN_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if os.environ.get("RENDER") == "true":
    try:
        User = get_user_model()
        if not User.objects.filter(username=os.environ.get("DJANGO_SUPERUSER_USERNAME")).exists():
            User.objects.create_superuser(
                os.environ.get("DJANGO_SUPERUSER_USERNAME"),
                os.environ.get("DJANGO_SUPERUSER_EMAIL"),
                os.environ.get("DJANGO_SUPERUSER_PASSWORD")
            )
    except Exception as e:
        print(f"Error creating superuser: {e}")
