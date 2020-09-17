"""
Django settings for edgebox_final project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# 宏
import sys
import logging
import django
from logging.handlers import RotatingFileHandler

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_FILES_DIR = os.path.join(os.path.dirname(BASE_DIR), "DATA/temp_files")  # 文件暂存路径
FAIL_FILES_DIR = os.path.join(os.path.dirname(BASE_DIR), "DATA/fail_files")  # 文件解析

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i(67r0=ud0l6ti(1sr&d0)m6fl6+_^bus41y&h92%i_ynp(-ov'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'User',
    "Agent",
    "Device",
    "Drive",
    "Log",
    "remotely",
    "SmartDevice",
    'djcelery',

    'rest_framework',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_swagger',  # 新增
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  #
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edgebox_final.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'SmartDevice/templates')],
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

WSGI_APPLICATION = 'edgebox_final.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'slave1': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

# django认证系统使用的模型类
AUTH_USER_MODEL = 'User.User'
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/10",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 分页的设置
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',  # 启动 drf 基于NameSpace的版本控制
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema'
}

DATABASE_ROUTERS = ["mydbrouter.Router"]

from .celery_config import *

# 宏
# # 邮箱服务器配置
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '10.129.4.95'
# # EMAIL_HOST = "smtp.foxconn.com"
EMAIL_PORT = 9090
# # 发送邮件的邮箱
EMAIL_HOST_USER = 'jackie.h.zhou@mail.foxconn.com'
# EMAIL_PASSWORD = 'Zouhong!286312'
EMAIL_FROM = 'EdgeBox_admin<%s>' % EMAIL_HOST_USER

# 刷新登录状态
LOGIN_REFRESH_TIME = 2 * 60  # 刷新登录状态2分钟
LOGIN_URL = "apis/user/login"

# logger设定
maxBytes = 100 * 1024 * 1024
backupCount = 10

# 登录验证码设置
VERIFY_CODE_WIDTH = 100  # 宽度
VERIFY_CODE_HEIGHT = 30  # 高度


def logger_init(log_file_name):
    """初始化log打印容器"""
    if getattr(sys, 'frozen', False):
        log_file_dir = os.path.join(os.path.dirname(BASE_DIR), 'log').replace("\\", "/")
    else:
        log_file_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log').replace("\\", "/")
    if not os.path.exists(log_file_dir):
        os.makedirs(log_file_dir)
    logger = logging.getLogger(log_file_name.split(".")[0])
    logger.setLevel(level=logging.INFO)
    rFHandler = RotatingFileHandler(log_file_dir + "/%s" % log_file_name, maxBytes=maxBytes,
                                    backupCount=backupCount)
    rFHandler.setLevel(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s :[%(levelname)s] %(filename)s line:%(lineno)d %(message)s',
                                  '%Y-%m-%d %H:%M:%S')
    rFHandler.setFormatter(formatter)
    logger.addHandler(rFHandler)
    # logger.info("%s initialization..." % log_file_name.split(".")[0])
    return logger


collection_log_record = logger_init("collection.log")  # 采集日志logger
collection_log_record.info("collection.log initializing...")

transmission_log_record = logger_init("transmission.log")  # 传输日志logger
transmission_log_record.info("transmission.log initializing...")

system_log_record = logger_init("system.log")  # 系统日志logger
system_log_record.info("system.log initializing...")

network_log_record = logger_init("network.log")  # 网络日志
network_log_record.info("network.log initializing...")

privileges_log_record = logger_init("privileges.log")  # 权限日志
privileges_log_record.info("privileges.log initializing...")

event_log_record = logger_init("event.log")  # 事件日志
event_log_record.info("privileges.log initializing...")

logger_dict = {
    1: collection_log_record,
    2: transmission_log_record,
    3: system_log_record,
    4: network_log_record,
    5: privileges_log_record,
    6: event_log_record
}

from .celery_config import *


def check_collect_enable(conn, sub_device_name):
    """
    检查采集使能
    :param conn:
    :param sub_device_name:
    :return:
    """

    collect_enable = conn.hget(sub_device_name, "collect_enable").decode()
    device_enable = conn.hget(sub_device_name, "device_enable").decode()
    if collect_enable == "True":
        collect_enable = True
    elif collect_enable == "False":
        collect_enable = False
    else:
        collect_enable = False
    if device_enable == "True":
        device_enable = True
    elif device_enable == "False":
        device_enable = False
    else:
        device_enable = False
    if not device_enable:
        # 总开关禁用
        enable = False
    else:
        # 总开关启用
        if collect_enable:
            enable = True
        else:
            enable = False
    return enable
