# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from base import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
PROJECT_APPS = ('ipvsstat',);


INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

