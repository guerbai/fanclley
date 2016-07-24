# -*- coding:utf-8 -*-
from app import celery
from flask import current_app
from origins import *
from sendemail import sendto_kindle
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@celery.task
def hardtask(kindle_loc,origin,bookid,bookname):

    if origin == u'起点':
        task = QidianFree(bookid,bookname)
    elif origin == u'红袖':
        task = HongxiuFree(bookid,bookname)
    elif origin == u'17K':
        task = Seventeenfree(bookid,bookname)
    elif origin == u'纵横':
        task = Zonghengfree(bookid,bookname)
    else:
        task = ''
    bname = origin+'_'+bookname
    task.get_info()
    task.generate_txt()
    bname = origin+'_'+bookname
    #几行命令行指令，生成epub，再生成mobi，然后删除txt和epub文件，最后发送至kindle邮箱。
    subprocess.call('pandoc app/data/txt/%s.txt -o app/data/mobiworkshop/%s.epub'%(bname,bname),shell=True)
    subprocess.call('rm app/data/txt/%s.txt'%bname,shell=True)
    subprocess.call('app/data/mobiworkshop/kindlegen -c2 app/data/mobiworkshop/%s.epub'%bname,shell=True)
    subprocess.call('rm app/data/mobiworkshop/%s.epub'%bname,shell=True)
    sendto_kindle(kindle_loc,bname)

    return {'status': 'Task completed!'}

