# -*- coding:utf-8 -*-
import logging
import time

#用来记录main blueprint的logger实例.
mainlogger = logging.getLogger('app.main')
mainlogger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./app/data/log/'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'mainlog.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

mainlogger.addHandler(fh)
mainlogger.addHandler(ch)

#用来记录origin 模块的logger实例.
orilogger = logging.getLogger('app.origin')
orilogger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./app/data/log/'+time.strftime("%Y-%m-%d %H:%M", time.localtime())+'originlog.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)


orilogger.addHandler(fh)
orilogger.addHandler(ch)
