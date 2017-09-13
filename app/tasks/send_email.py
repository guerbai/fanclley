# -*- coding:utf-8 -*-
from jinja2 import Template
import os
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
from ..extentions import celery


mail_config = {
        'from_addr': 'fanclley@163.com',
        'password': os.environ.get('MAIL_PASSWORD'),
        'smtp_server': 'smtp.163.com',
    }


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((name, addr))


def send_email(msg, to_addr):
    smtp_server, from_addr, password = \
        mail_config['smtp_server'], mail_config['from_addr'], mail_config['password']
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


# TODO: give specific templates_dir
def construct_content(template, **kwargs):
    templates_dir = ''
    with open(templates_dir+template+'.html', 'r') as f:
        template = Template(f.read())
        return template.render(**kwargs)


def normal_msg(to_addr, subject, template, **kwargs):
    content = construct_content(template, **kwargs)
    msg = MIMEText(content)
    msg['From'] = email_config['from_addr']
    msg['To'] = to_addr
    msg['Subject'] = Header(subject, 'utf-8').encode()
    return msg


def book_msg(to_addr, book):
    # TODO: Give a subject.
    subject = ''
    mobi_workshop_dir = '../../mobi_workshop/'
    bookname = book+'.mobi'
    msg = MIMEMultipart()
    msg['From'] = mail_config['from_addr']
    msg['To'] = to_addr
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
    # TODO: check if target is 0kb, if so, send_alert.
    with open(mobi_workshop_dir+book+'.mobi', 'rb') as f:
        mime = MIMEBase('*', '*/*', filename=bookname)
        mime.add_header('Content-Disposition', 'attachment', filename=bookname)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)
    return msg


@celery.task()
def send_normal_email(to_addr, subject, template, **kwargs):
    msg = normal_msg(to_addr, subject, template, **kwargs)
    send_email(msg, to_addr)


@celery.task()
def send_to_kindle(to_addr, book):
    msg = book_msg(to_addr, book)
    send_email(msg, to_addr)
