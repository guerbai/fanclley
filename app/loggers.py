#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import time

class my_logger:

    def __init__(self,logername):
        self.logger = logging.getLogger('app.'+logername)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('./app/data/log/' + time.strftime("%Y-%m-%d", time.localtime()) +logername+'.log')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

#mainlogger = my_logger('main').logger
orilogger = my_logger('origin').logger
#authlogger = my_logger('auth').logger
'''
#用来记录main blueprint的logger实例.
mainlogger = logging.getLogger('app.main')
mainlogger.setLevel(logging.DEBUG)
main_fh = logging.FileHandler('./app/data/log/'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'mainlog.log')
main_fh.setLevel(logging.DEBUG)

main_ch = logging.StreamHandler()
main_ch.setLevel(logging.DEBUG)

main_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
main_fh.setFormatter(main_formatter)
main_ch.setFormatter(main_formatter)

mainlogger.addHandler(main_fh)
mainlogger.addHandler(main_ch)

#用来记录origin 模块的logger实例.
orilogger = logging.getLogger('app.origin')
orilogger.setLevel(logging.DEBUG)
ori_fh = logging.FileHandler('./app/data/log/'+time.strftime("%Y-%m-%d %H:%M", time.localtime())+'originlog.log')
ori_fh.setLevel(logging.DEBUG)

ori_ch = logging.StreamHandler()
ori_ch.setLevel(logging.DEBUG)

ori_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ori_fh.setFormatter(ori_formatter)
ori_ch.setFormatter(ori_formatter)


orilogger.addHandler(ori_fh)
orilogger.addHandler(ori_ch)

#用来记录auth blueprint的logger实例.
authlogger = logging.getLogger('app.auth')
authlogger.setLevel(logging.DEBUG)
auth_fh = logging.FileHandler('./app/data/log/'+time.strftime("%Y-%m-%d %H:%M", time.localtime())+'authlog.log')
auth_fh.setLevel(logging.DEBUG)

auth_ch = logging.StreamHandler()
auth_ch.setLevel(logging.DEBUG)

auth_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
auth_fh.setFormatter(auth_formatter)
auth_ch.setFormatter(auth_formatter)


authlogger.addHandler(auth_fh)
authlogger.addHandler(auth_ch)'''