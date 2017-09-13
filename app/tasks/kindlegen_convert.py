# -*- coding:utf-8 -*-
import os
from .send_email import send_to_kindle
from ..extentions import celery

workdir = '../../mobiworkshop/'

def use_kindlegen(bname):
    os.system('pandoc %s%s.txt -o %s%s.epub'%(workdir,bname,workdir,bname))
    os.system('rm %s%s.txt'%(workdir,bname))
    os.system('%skindlegen %s%s.epub'%(workdir,workdir,bname))
    os.system('rm %s%s.epub'%(workdir,bname))



# @celery.task
# def hardtask(kindle_loc,origin,bookid,bookname):
#     if '(' in bookname:
#         bookname = bookname.replace('(','.')
#     if ')' in bookname:
#         bookname = bookname.replace(')', '.')
#     if '（' in bookname:
#         bookname = bookname.replace('（', '.')
#     if '）' in bookname:
#         bookname = bookname.replace('）', '.')
#     if origin == u'起点':
#         task = QidianFree(bookid,bookname)
#     elif origin == u'红袖':
#         task = HongxiuFree(bookid,bookname)
#     elif origin == u'17K':
#         task = Seventeenfree(bookid,bookname)
#     elif origin == u'纵横':
#         task = Zonghengfree(bookid,bookname)
#     else:
#         task = ''
#     task.get_info()
#     task.generate_txt()
#     bname = origin+u'_'+bookname
#     #几行命令行指令，生成epub，再生成mobi，然后删除txt和epub文件，最后发送至kindle邮箱。

#     subprocess.call('pandoc %s%s.txt -o %s%s.epub'%(workdir,bname,workdir,bname),shell=True)
#     subprocess.call('rm %s%s.txt'%(workdir,bname),shell=True)
#     subprocess.call('%skindlegen %s%s.epub'%(workdir,workdir,bname),shell=True)
#     subprocess.call('rm %s%s.epub'%(workdir,bname),shell=True)
#     sendto_kindle(kindle_loc,bname)
#     #subprocess.call('rm %s%s.mobi'%(workdir,bname),shell=True)

#     return {'status': 'Task completed!'}

