# -*- coding:utf-8 -*-
import logging
from cloghandler import ConcurrentRotatingFileHandler as RFHandler
from .singleton import Singleton


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
        	cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

            
class FanclleyLogger(Singleton):

    def __init__(self):
        logger = logging.getLogger()
        logger.propagate = False
        formatter = logging.Formatter('%(levelname)s-%(asctime)s-%(funcName)s-%(message)s')

        filehandler = RFHandler("/var/log/fanclley.log",'a',1*1024*1024, 10000)
        filehandler.setFormatter(formatter)
        filehandler.suffix = "%Y%m%d-%H%M.log"
        logger.setLevel(logging.INFO)
        logger.addHandler(filehandler)

        terminal_handler = logging.StreamHandler()
        terminal_handler.setFormatter(formatter)
        terminal_handler.setLevel(logging.DEBUG)
        logger.addHandler(terminal_handler)

        self._logger = logger

    def get_logger(self):
        return self._logger

logger = FanclleyLogger().get_logger()

__all__ = ['logger']