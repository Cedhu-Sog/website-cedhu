from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Clave secreta
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

# 🐞 DEBUG SIEMPRE TRUE EN LOCAL
DEBUG = os.environ.get("DEBUG", "True") == "True"

# 🌍 Hosts permitidos
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'www.cedhu.edu.co',
    'cedhu.edu.co',
    'website-cedhu.onrender.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://website-cedhu-production.up.railway.app',
    'https://www.cedhu.edu.co',
    'https://cedhu.edu.co',
]

# 📦 Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🔄 Solo para desarrollo (recarga automática)
    'django_browser_reload',

    # App principal
    'core',
]

# 🧱 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise solo sirve en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Browser reload (dev)
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'config.urls'

# 🎨 Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# 🗄️ Base de datos (LOCAL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'cedhu_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'cotamo123'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}



# 🔐 Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌐 Idioma y zona horaria
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 📁 Archivos estáticos
STATIC_URL = '/static/'

# Desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static'
]

# Producción
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ⚠️ SOLO EN PRODUCCIÓN
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 🖼️ Media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔑 Login
LOGIN_URL = '/login/'

# 🔢 ID por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 💳 Stripe
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')


