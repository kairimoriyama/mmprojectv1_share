from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 暫定（for share）
SECRET_KEY = 'SECRET_KEY'

# ログインできるemailのドメインを制限（adapter.pyで管理）
SOCIALACCOUNT_ADAPTER = 'mmproject.adapter.CustomSocialAccountAdapter'
# 以下は利用できなかった
# SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS= ['gmail.com'] 

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
        'DIRS': [ BASE_DIR/ 'templates' ],
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

AUTH_USER_MODEL = 'accounts.User'



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

USE_TZ = False

# django.contrib.humanize tmplateでカンマ区切り
NUMBER_GROUPING = 3

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (BASE_DIR/ "static",)

MEDIA_URL = '/media/'


AUTH_USER_MODEL = 'accounts.CustomUser'


#ログイン不要なURL
PUBLIC_PATHS = [
    '/admin/',
    '/p-admin/',
	'/accounts/',
    '/accounts.google.com/',
]

SITE_ID = 1
# ログイン・ログアウト後の画面
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'


AUTHENTICATION_BACKENDS = (
    # 管理サイト用
    'django.contrib.auth.backends.ModelBackend',
    # 一般ユーザー用
    'allauth.account.auth_backends.AuthenticationBackend',
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



# image resize django_resized
DJANGORESIZED_DEFAULT_SIZE = [1600, 1200]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = False
