# -*- coding:utf-8 -*-
from flask import Flask
from celery import Celery
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message(app.config['FANCLLEY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#                   sender=app.config['FANCLLEY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr


# def sendto_kindle(to, bookname):
#     #搞一个局部的app。
#     app = create_app('production')
#     msg = Message(app.config['FANCLLEY_MAIL_SUBJECT_PREFIX']+ ' ' + u'Your book coming!',
#                   sender=app.config['FANCLLEY_MAIL_SENDER'], recipients=[to])
#     msg.body = u"fanclley"
#     msg.html = u"<b>Fanclley provide this service for you!</b>"
#     with app.open_resource(u"data/mobiworkshop/" + bookname + u'.mobi') as fp:
#         msg.attach(u'fanclley.mobi', "*/*", fp.read())
#     #mail.send()
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((name, addr))


@celery.task()
def send_email(to_addr, subject, template, **kwargs):
    from_addr = 'fanclley@163.com'
    password = 'L501826'
    to_addr = '617243899@qq.com'
    smtp_server = 'smtp.163.com'

    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'Python爱好者 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    # msg['From'] = from_addr
    # msg['To'] = to_addr
    msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def send_to_kindle(to_addr, bookname):
    from_addr = 'fanclley@163.com'
    password = 'L501826'
    to_addr = '617243899@qq.com'
    smtp_server = 'smtp.163.com'

    # 邮件对象:
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'Python爱好者 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

    # 邮件正文是MIMEText:
    msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open('./taskhandler.py', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', '*/*', filename='test.py')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='test.py')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()


@app.route('/')
def index():
    send_email.delay(0, 0, 0)
    return 'ok'

    
if __name__ == '__main__':
    # send_email(0, 0, 0)
    # send_to_kindle(0, 0)
    __name__ = 'sendemail'
    app.run(debug=True)
