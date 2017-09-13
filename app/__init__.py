# -*- coding: utf-8 -*-
from flask import Flask, request
import os
import logging
import time
from functools import partial
from flask_login import current_user
from wxpy import get_wechat_logger


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.error_logger = get_wechat_logger()

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    celery.conf.update(app.config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


def create_app(config=None):
    app = Flask("fanclley")

    configure_app(app, config)
    configure_celery_app(app, celery)
    configure_blueprints(app)
    configure_extensions(app)
    configure_template_filters(app)
    configure_context_processors(app)
    configure_before_handlers(app)
    configure_errorhandlers(app)
    configure_logging(app)

    return app


def configure_app(app, config):
    """Configures FlaskBB."""
    # Use the default config and override it afterwards
    app.config.from_object('flaskbb.configs.default.DefaultConfig')

    if isinstance(config, string_types) and \
            os.path.exists(os.path.abspath(config)):
        config = os.path.abspath(config)
        app.config.from_pyfile(config)
    else:
        # try to update the config from the object
        app.config.from_object(config)
    # Add the location of the config to the config
    app.config["CONFIG_PATH"] = config

    # try to update the config via the environment variable
    app.config.from_envvar("FLASKBB_SETTINGS", silent=True)

    # Parse the env for FLASKBB_ prefixed env variables and set
    # them on the config object
    app_config_from_env(app, prefix="FLASKBB_")


def configure_celery_app(app, celery):
    """Configures the celery app."""
    app.config.update({'BROKER_URL': app.config["CELERY_BROKER_URL"]})
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


def configure_blueprints(app):
    app.register_blueprint(forum, url_prefix=app.config["FORUM_URL_PREFIX"])
    app.register_blueprint(user, url_prefix=app.config["USER_URL_PREFIX"])
    app.register_blueprint(auth, url_prefix=app.config["AUTH_URL_PREFIX"])
    app.register_blueprint(
        management, url_prefix=app.config["ADMIN_URL_PREFIX"]
    )
    app.register_blueprint(
        message, url_prefix=app.config["MESSAGE_URL_PREFIX"]
    )


def configure_extensions(app):
    """Configures the extensions."""

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Mail
    mail.init_app(app)


    # Flask-Login
    login_manager.session_protection = 'strong'
    login_manager.login_view = app.config["LOGIN_VIEW"]
    login_manager.refresh_view = app.config["REAUTH_VIEW"]
    login_manager.login_message_category = app.config["LOGIN_MESSAGE_CATEGORY"]
    login_manager.needs_refresh_message_category = \
        app.config["REFRESH_MESSAGE_CATEGORY"]
    login_manager.anonymous_user = Guest

    @login_manager.user_loader
    def load_user(user_id):
        """Loads the user. Required by the `login` extension."""

        user_instance = User.query.filter_by(id=user_id).first()
        if user_instance:
            return user_instance
        else:
            return None

    login_manager.init_app(app)


def configure_context_processors(app):
    """Configures the context processors."""

    @app.context_processor
    def inject_flaskbb_config():
        return dict(fanclley_config=fanclley_config, format_date=format_date)


def configure_before_handlers(app):
    """Configures the before request handlers."""

    @app.before_request
    def before_request():
        pass


def configure_errorhandlers(app):
    """Configures the error handlers."""

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("500.html"), 500


def configure_logging(app):
    """Configures logging."""

    logs_folder = os.path.join(app.root_path, os.pardir, "logs")
    from logging.handlers import SMTPHandler
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    info_log = os.path.join(logs_folder, app.config['INFO_LOG'])

    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(logs_folder, app.config['ERROR_LOG'])

    error_file_handler = logging.handlers.RotatingFileHandler(
        error_log,
        maxBytes=100000,
        backupCount=10
    )

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    if app.config["SEND_LOGS"]:
        mail_handler = \
            SMTPHandler(
                app.config['MAIL_SERVER'],
                app.config['MAIL_DEFAULT_SENDER'],
                app.config['ADMINS'],
                'application error, no admins specified',
                (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            )

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)

    if app.config["SQLALCHEMY_ECHO"]:
        # Ref: http://stackoverflow.com/a/8428546
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement,
                                  parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement,
                                 parameters, context, executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
    app.logger.debug("Total Time: %f", total)