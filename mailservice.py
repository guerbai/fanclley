#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_mail import Mail,Message
app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.qq.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = '617243899@qq.com',
    MAIL_PASSWORD = 'pgofcpkadcdibcfc',
))
mail = Mail(app)


@app.route("/")
def index():

    msg = Message("Hello",
                  sender="617243899@qq.com",
                  recipients=["fyb617243899@kindle.cn"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    with app.open_resource(u"novel.txt") as fp:
        msg.attach(u"novel.txt","text/*", fp.read())
    mail.send(msg)
    return 'hello fanclley'

if __name__ == '__main__':
    app.run(debug=True)