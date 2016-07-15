import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '617243899@qq.com'  # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'pgofcpkadcdibcfc'  # os.environ.get('MAIL_PASSWORD')
    MAIL_ASCII_ATTACHMENTS = True
    FANCLLEY_MAIL_SUBJECT_PREFIX = '[Fanclley]'
    FANCLLEY_MAIL_SENDER = 'Fanclley Admin <617243899@qq.com>'
    FANCLLEY_ADMIN = '617243899@qq.com'
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}