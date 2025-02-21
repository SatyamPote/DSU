import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Ensures BASE_DIR is properly set

DEBUG = True  # Make sure you set it to False for production

ALLOWED_HOSTS = ['*']  # Replace 'yourdomain.com' with your actual domain


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ROOT_URLCONF = 'cst_notes.urls'  # Change 'cst_notes' to your project's name


# Static & Media Files Configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
