# -*- coding: utf-8 -*-
import os
import sys
import datetime


basedir = os.path.abspath(os.path.dirname(__file__))

basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                           os.path.dirname(__file__)))))


class Config(object):


    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/' + \
                              'fanclley.sqlite'

    SQLALCHEMY_ECHO = False

    # Security
    # ------------------------------
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # You can generate the WTF_CSRF_SECRET_KEY the same way as you have
    # generated the SECRET_KEY. If no WTF_CSRF_SECRET_KEY is provided, it will
    # use the SECRET_KEY.
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    #mail.
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fanclley@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = True
    MAIL_DEFAULT_SENDER = ("Default Sender", "noreply@example.org")

    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    if not REDIS_ENABLED: CELERY_ALWAYS_EAGER = True

    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    FANCLLEY_MAIL_SUBJECT_PREFIX = '[Fanclley]'
    FANCLLEY_MAIL_SENDER = 'Fanclley Admin <fanclley@163.com>'
    FANCLLEY_ADMIN = 'fanclley@163.com'
