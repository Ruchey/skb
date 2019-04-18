from skb.settings import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.0.157']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SITE_ID = 3

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}