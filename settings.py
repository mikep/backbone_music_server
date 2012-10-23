# Django settings for first project.
import errno
import logging
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

MUSIC_APP_ROOT = os.path.join('srv','www')

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SECRET_KEY = '-a(8*t%%zr8i+#r$_jt8!fdbe1ypyryu8c$r1(=+4&0-+9b$zd'

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
)

LOG_FILENAME = "/var/log/nginx/music.log"

if not os.path.exists(LOG_FILENAME):
    try:
        os.makedirs(os.path.dirname(LOG_FILENAME))
    except OSError as e:
        if e.errno == errno.EEXIST: # File exists - do nothing
            pass
        else:
            raise

# get the corresponding enum value from loggging
# default to INFO log level
loglevel = getattr(logging, 'INFO')

root_logger = logging.getLogger('')
root_logger.setLevel(loglevel)

handler = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(process)d %(name)s %(message)s')
handler.setFormatter(formatter)

root_logger.addHandler(handler)

