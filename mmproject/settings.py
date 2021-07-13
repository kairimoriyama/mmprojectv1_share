from .settings_common import *
import os

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

    'django_ses',
    'django.contrib.humanize',
    'django_resized',
]


# デバッグモードを有効にするかどうか(本番運用では必ずFalseにする)
DEBUG = False


# The maximum number of parameters that may be received via GET or POS
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000


# 許可するホスト名のリスト
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mmproject',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}


# 静的ファイルを配置する場所
STATIC_ROOT = '/usr/share/nginx/html/static'
MEDIA_ROOT = '/usr/share/nginx/html/media'


