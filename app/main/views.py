from flask import render_template, session, redirect, url_for, current_app
from ..email import send_email
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    send_email()
    return 'hello fanclley'