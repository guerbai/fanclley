# -*- coding: utf-8 -*-
from celery import Celery
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from flask_wtf.csrf import CSRFProtect

bootstrap = BootStrap()

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# Mail
mail = Mail()

# CSRF
csrf = CSRFProtect()

# Celery
celery = Celery("fanclley", broker='')