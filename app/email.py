#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail
import time


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(bookname):
    app = current_app._get_current_object()
    msg = Message("Hello",
                  sender="617243899@qq.com",
                  recipients=["fyb617243899@kindle.cn",
                              "15140327802@163.com"])
    msg.body = "fanclley"
    msg.html = "<b>testing</b>"
    with app.open_resource(u"data/txt/"+bookname+'.txt') as fp:
        msg.attach('fanclley'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'.txt', "*/*", fp.read())
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr