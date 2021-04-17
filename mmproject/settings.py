from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l!@oqrwyn(lxw3)hw5ii_xlds-)4c5d+kb0o!b4^%(3hgaevgl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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
<<<<<<< HEAD

]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
    'SCOPE': [
        'profile',
        'email',
    ],
    'AUTH_PARAMS': {
        'access_type': 'online',
    }
    }
}

MIDDLEWARE = [
    'global_login_required.GlobalLoginRequiredMiddleware', #一括ログイン
=======
]

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#     'SCOPE': [
#         'profile',
#         'email',
#     ],
#     'AUTH_PARAMS': {
#         'access_type': 'online',
#     }
# }
# }

MIDDLEWARE = [
>>>>>>> origin/main
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mmproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'mmproject.wsgi.application'

<<<<<<< HEAD
AUTH_USER_MODEL = 'accounts.User'
=======
>>>>>>> origin/main

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
<<<<<<< HEAD
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mmproject',
        'USER': 'postgres',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
=======
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
>>>>>>> origin/main
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join( BASE_DIR,'media')
MEDIA_URL = '/media/'


<<<<<<< HEAD

AUTH_USER_MODEL = 'accounts.CustomUser'


#ログイン不要なURL
PUBLIC_PATHS = [
	'/accounts/',
    '/admin/',
    '/accounts.google.com/',
]

SITE_ID = 1
# ログイン・ログアウト後の画面
LOGIN_REDIRECT_URL = '/'
=======
AUTH_USER_MODEL = 'accounts.CustomUser'

SITE_ID = 1
# ログイン・ログアウト後の画面
LOGIN_REDIRECT_URL = 'home'
>>>>>>> origin/main
LOGIN_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'


<<<<<<< HEAD

AUTHENTICATION_BACKENDS = (
    # 管理サイト用
    'django.contrib.auth.backends.ModelBackend',
    # 一般ユーザー用
    'allauth.account.auth_backends.AuthenticationBackend',
=======
AUTHENTICATION_BACKENDS = (
    # 一般ユーザー用
    'allauth.account.auth_backends.AuthenticationBackend',
    # 管理サイト用
    'django.contrib.auth.backends.ModelBackend',
>>>>>>> origin/main
)

# 認証方法 メールアドレス
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# ユーザー確認のメール送信(none=送信しない, mandatory=送信する)
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True

# # 開発中はemail送信ではなくコンソールへの表示で対応
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



# ログアウト処理の方法
ACCOUNT_LOGOUT_ON_GET =True

