# import drf_yasg
# import db_router

# SECRET_KEY = 'r62wlc+&(^_4g-_2)so0z&53_e*u7+jy#=q^-y=ayd2y9jqv5m'

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'drf_yasg',
#     'django_extensions',
#     # Your apps
#     'patents',
#     'trademarks',
# ]
# DEBUG = True
# # URL to use when referring to static files
# STATIC_URL = '/static/'


# REST_FRAMEWORK = {
#     'DEFAULT_FILTER_BACKENDS': [
#         'django_filters.rest_framework.DjangoFilterBackend'
#     ],
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         # Comment out the BrowsableAPIRenderer if you don't want to support it
#         # 'rest_framework.renderers.BrowsableAPIRenderer',
#     ]
# }


# # Swagger settings (optional)
# SWAGGER_SETTINGS = {
#     'SECURITY_DEFINITIONS': {
#         'Basic': {
#             'type': 'basic'
#         }
#     },
# }

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Ensure this line is present
#         'DIRS': [],  # You can add template directories here if needed
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',  # Must be included
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',  # Must be included
#     'django.contrib.messages.middleware.MessageMiddleware',  # Must be included
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
# ALLOWED_HOSTS = ['127.0.0.1', '10.10.1.10', '38.111.99.214', 'localhost']


# ROOT_URLCONF = 'DB_Main.urls'
# WSGI_APPLICATION = 'DB_Main.wsgi.application'

# # Databases


# DATABASES = {
#     'default': { # This is patents db
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'Patents_db',
#         'USER': 'Azhari',
#         'PASSWORD': 'CIPO',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     },
#     'trademarks_db': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'Trademarks_db',
#         'USER': 'Azhari',
#         'PASSWORD': 'CIPO',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# DATABASE_ROUTERS = ['db_router.DBRouter']

# # Password validation
# # https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/5.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         },
#     },
# }

import drf_yasg
import os
from dotenv import load_dotenv

load_dotenv()
# Removed: import db_router

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'django_extensions',
    'django_filters',
    'corsheaders',
    # Your apps
    'trademarks',
]

DEBUG = os.getenv('DEBUG', 'False') == 'True'

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'trademarks.pagination.FlexiblePageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',  # Uncomment if needed
    ]
}


SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "DB_Main.urls.schema_info",
    "DEFAULT_MODEL_RENDERING": "example",
    "DOC_EXPANSION": "none",
    "REFETCH_SCHEMA_WITH_AUTH": False,
    "OPERATIONS_SORTER": "alpha",
    "USE_SESSION_AUTH": False,
    # Hide non‑GET by default
    "METHODS": ["get"],
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'DB_Main.urls'
WSGI_APPLICATION = 'DB_Main.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'TM_data'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'Mostafa75'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# DATABASE_ROUTERS = ['db_router.DBRouter']

# Removed DATABASE_ROUTERS setting

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
