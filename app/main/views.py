#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app
from ..email import send_email
from . import main
from ..origins.QidianFree import *
from ..origins.HongxiuFree import *


@main.route('/', methods=['GET', 'POST'])
def index():
    keyword_search_Qidian(u'永恒之心')
    a = QidianFree(0)
    a.generate_txt()
    #send_email(a.bookname)
    #app.logger.info('hi,there!')

    return 'hello fanclley'