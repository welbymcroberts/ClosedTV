DEBUG = False
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-GB'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'ClosedTV.middleware.TimerMiddleware',
    'ClosedTV.middleware.GitMiddleware',
)
ROOT_URLCONF = 'ClosedTV.urls'
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'ClosedTV.main'
)

try:
    from local_settings import *
except ImportError:
    pass




import subprocess as sp
GIT_SHA = sp.Popen(['git', '--git-dir', BASE_DIR+'/.git', 'rev-parse', 'HEAD'], stdout=sp.PIPE).communicate()[0].strip()


