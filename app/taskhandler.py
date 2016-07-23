# -*- coding:utf-8 -*-
from app import celery
from origins import *
from sendemail import sendto_kindle
import os
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
    task.get_info()
    task.generate_txt()
    print kindle_loc

    return {'status': 'Task completed!'}