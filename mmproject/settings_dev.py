from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'goodidea.apps.GoodideaConfig',
    'accounts.apps.AccountsConfig',
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    #'django_ses',
]



ALLOWED_HOSTS = []
