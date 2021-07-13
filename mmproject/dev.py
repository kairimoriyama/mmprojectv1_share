from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# The maximum number of parameters that may be received via GET or POS
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000


# Application definition

INSTALLED_APPS = [
    'goodidea.apps.GoodideaConfig',
    'receipt.apps.ReceiptConfig',
    'procurement.apps.ProcurementConfig',
    'bankaccount.apps.BankaccountConfig',
    'stylistdivision.apps.StylistdivisionConfig',
    'staffdb.apps.StaffdbConfig',
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
    'django.contrib.humanize',
    'django_resized',
]


ALLOWED_HOSTS = []



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = BASE_DIR/ 'media'