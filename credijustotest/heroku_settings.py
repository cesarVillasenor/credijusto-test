import dj_database_url

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = True

SECRET_KEY = '58nbbt9+yr_@jiq$q*lshgam=un*)-e)*5++zli_idts4tjv7b'
NEVERCACHE_KEY = "#ao%db)h2ug&a$kesg_rc@1qe@ckw4z8ksu=2zu&f!(6)1l--&"
BANXICO_TOKEN = "be2017c7e43a691adc97b469cd547609da39b3e754ce11fe8de5f10ac7ed2bfa"
FIXER_ACCESS_KEY = '6d798b53a4713a3b9335aede2795c0d7'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ddu4aqs63j5t',
        'USER': 'wddlrpbsolocim',
        'PASSWORD': '60d4279d95531073b15d8ba717a235f6a9725f20f161916d762e13c73d77de02',
        'HOST': 'ec2-54-156-73-147.compute-1.amazonaws.com',
        'PORT': '5432',
    },
}

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

ALLOWED_HOSTS = ['credijusto-test.herokuapp.com', "localhost", "127.0.0.1", "::1"]