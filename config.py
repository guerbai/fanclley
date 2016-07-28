#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:


    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you can not guess this.'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    #mail.
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fanclley@163.com'#os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'L501826'#os.environ.get('MAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = True
    FANCLLEY_MAIL_SUBJECT_PREFIX = '[Fanclley]'
    FANCLLEY_MAIL_SENDER = 'Fanclley Admin <fanclley@163.com>'
    FANCLLEY_ADMIN = 'fanclley@163.com'
    #celery.
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TASK_SERIALIZER = 'json'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FANCLLEY_MAIL_SENDER,
            toaddrs=[cls.FANCLLEY_ADMIN],
            subject=cls.FANCLLEY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}