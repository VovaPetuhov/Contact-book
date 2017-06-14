DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'contactsdb',
        'USER': 'root',
        'PASSWORD': '431790',
        'HOST': '127.0.0.1',
    }
}

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/login/'

