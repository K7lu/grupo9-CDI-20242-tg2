import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

SECRET_KEY = 'sua-chave-secreta'  # Troque por uma chave secreta gerada de forma segura

DEBUG = True

ALLOWED_HOSTS = []

# URL para onde redirecionar usuários não autenticados
LOGIN_URL = '/login/'

# URL para redirecionar após login bem-sucedido
LOGIN_REDIRECT_URL = '/clients/'  # Altere para a rota desejada após o login

# URL para redirecionar após logout
LOGOUT_REDIRECT_URL = '/login/'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clients',
    'departments',
    'employees',
    'projects',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'sger.wsgi.application'

# Database configuration for MariaDB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Usamos 'mysql' porque MariaDB é compatível com MySQL
        'NAME': 'sger_db',               # Substitua pelo nome do seu banco de dados
        'USER': 'admin',            # Substitua pelo seu usuário do MariaDB
        'PASSWORD': 'admin',          # Substitua pela sua senha
        'HOST': 'localhost',                   # Ou o endereço IP do servidor de banco de dados
        'PORT': '3306',                        # Porta padrão do MariaDB
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Defina o diretório onde os arquivos estáticos serão coletados para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Adicione o diretório de arquivos estáticos adicionais (por exemplo, para CSS, JS personalizados)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Define o caminho para o diretório de mídia, onde arquivos de usuário podem ser armazenados
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Caso queira usar o PyMySQL, adicione este trecho no início do arquivo para evitar o erro do MySQLdb
# import pymysql
# pymysql.install_as_MySQLdb()

# Configurações de segurança adicionais
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
