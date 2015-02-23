"""
Django settings for aviastudent_backend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^=i_&yg&t=^0dm+(j)d%8ah68n#s0xm*p#grz9n7uq+i5i8bw*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'aviastudent_backend'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aviastudent_backend.urls'

WSGI_APPLICATION = 'aviastudent_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aviastudent',
        'USER': 'postgres',
        'PASSWORD': 'aviastudent',
        'HOST': '127.0.0.1'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

try:
    import aviastudent_backend.facebook_credentials
    SOCIAL_AUTH_FACEBOOK_KEY = aviastudent_backend.facebook_credentials.SOCIAL_AUTH_FACEBOOK_KEY
    SOCIAL_AUTH_FACEBOOK_SECRET = aviastudent_backend.facebook_credentials.SOCIAL_AUTH_FACEBOOK_SECRET
except:
    print('Facebook credentials are not found')

try:
    import aviastudent_backend.google_credentials
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = aviastudent_backend.google_credentials.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = aviastudent_backend.google_credentials.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
except:
    print('Google credentials are not found')

try:
    import aviastudent_backend.twitter_credentials
    SOCIAL_AUTH_TWITTER_KEY = aviastudent_backend.twitter_credentials.SOCIAL_AUTH_TWITTER_KEY
    SOCIAL_AUTH_TWITTER_SECRET = aviastudent_backend.twitter_credentials.SOCIAL_AUTH_TWITTER_SECRET
except:
    print('Twitter credentials are not found')
