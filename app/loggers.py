#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import time
from celery.utils.log import get_task_logger

class my_logger:

    def __init__(self,loggername):
        self.logger = logging.getLogger('app.'+loggername)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('./app/data/log/' + time.strftime("%Y-%m-%d", time.localtime()) +loggername+'.log')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

orilogger = my_logger('origin').logger
#authlogger = my_logger('auth').logger
