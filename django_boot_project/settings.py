"""
Django settings for django_boot_project project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^19(1s24ufk7olxdvhz!-6jat%43x%035d3svf$r8%$s00dg!v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'demo',
    'django_boot',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'bootstrap4',
    'fontawesome_5',
    'mptt',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_boot_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'loaders': [
                'apptemplates.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_boot_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django_boot

DB_NAVBAR_MENU = [
    {
        'name': '控制台',
        'url': '/home/',
        'highlight': '/home/',
        'icon': 'home',
        'permission': None
    },
    {
        'name': '系统管理',
        'icon': 'cogs',
        'children': [
            {
                'name': '用户',
                'url': '/auth/user/',
                'highlight': '/auth/user/',
                'permission': 'auth.can_view_user'
            },
            {
                'name': '组',
                'url': '/auth/group/',
                'highlight': '/auth/group/',
                'permission': 'auth.can_view_group'
            },
            {
                'name': '字典',
                'url': '/db/dict/',
                'highlight': '/db/dict/',
                'permission': 'db.can_view_dict'
            },
            {
                'name': '组织',
                'url': '/db/org/',
                'highlight': '/db/org/',
                'permission': 'db.can_view_org'
            },
            {
                'name': '配置',
                'url': '/db/config/',
                'highlight': '/db/config/',
                'permission': 'db.can_view_config'
            },
        ]
    },
    {
        'name': '测试',
        'url': '/test/',
        'highlight': '/test/',
        'icon': 'flag',
        'permission': None
    }
]

DB_USER_MENU = [
    {
        'name': 'profile',
        'url': reverse_lazy('demo:profile')
    },
    {
        'name': 'change password',
        'url': reverse_lazy('admin:password_change')
    },
    {
        'name': '---',
    },
    {
        'name': 'logout',
        'url': reverse_lazy('admin:logout')
    },
]
