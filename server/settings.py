from datetime import timedelta
import os

DEFAULT_PERSON_ID = 0
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
ROOT_URLCONF = 'urls'
APPEND_SLASH = True

SECRET_KEY = 'gyuiofggfreaq7890yhuibt243BUISW9324809&soi$%*)w)ns;DGJ*(u)'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'database',
    #     'USER': 'test',
    #     'PASSWORD': '123456',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# TEMPLATES 配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('templates')],
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

# MIDDLEWARE 配置
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'person.Person'

INSTALLED_APPS = [
    'person',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'person.apps.PersonConfig',
    'trip',
    'album',
    'entry',
    'moment',
    'picture',
    
    'corsheaders',
]

CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://113.44.213.129:5172'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '113.44.213.129']

MEDIA_ROOT = '/img/'
MEDIA_URL = '/img/'
base_url = '113.44.213.129:5172'