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
    # app = current_app._get_current_object()
    # with app.app_context():
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
        bname = origin+'_'+bookname
        subprocess.call('pandoc app/data/txt/%s.txt -o app/data/mobiworkshop/%s.epub'%(bname,bname),shell=True)
        subprocess.call('app/data/mobiworkshop/kindlegen -c2 app/data/mobiworkshop/%s.epub'%bname,shell=True)
        sendto_kindle(kindle_loc,bname,app)

        return {'status': 'Task completed!'}
#bname = u'纵横_踢出个未来'
#subprocess.call('pandoc data/txt/%s.txt -o data/mobiworkshop/%s.epub'%(bname,bname),shell=True)
#subprocess.call('./data/mobiworkshop/kindlegen -c2 ./data/mobiworkshop/%s.epub'%bname,shell=True)