from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email():
    app = current_app._get_current_object()


    msg = Message("Hello",
                  sender="617243899@qq.com",
                  recipients=["fyb617243899@kindle.cn"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    with app.open_resource(u"data/norwegianwood.mobi") as fp:
        msg.attach(u"data/norwegianwood.mobi", "*/*", fp.read())

    mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr