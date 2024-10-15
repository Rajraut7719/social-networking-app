import os
from .settings import *

SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTSS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS =['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

connection_string = os.environ(['AZURE_POSTGRESQL_CONNECTIONSTRING'])
parameter = {pair.split('='):pair.split('=')[1] for pair in connection_string.split(' ')}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parameter['dbname'],
        "USER": parameter['user'],
        "PASSWORD": parameter['password'],
        "HOST": parameter['host'],
        "PORT": "5432",
        'OPTIONS': {
            'options': '-c search_path=social'
        },
    }
}
