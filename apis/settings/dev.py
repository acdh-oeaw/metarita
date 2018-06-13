from .base import *

SPARQL_ENDPOINT = 'https://bgdefc.eos.arz.oeaw.ac.at/sparql'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^mm-24*i-6iecm7c@z9l+7%^ns^4g^z!8=dgffg4ulggr-4=1%'
INSTALLED_APPS += ('django_extensions',)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['metarita.eos.arz.oeaw.ac.at', 'metarita.acdh.oeaw.at', '127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
