#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers  import orilogger
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")

class JinjiangFree:

    s = requests.session()
    origin_id = 2
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    _chap_list = []
    bookname = ''
    bookstatus = ''
    authorname = ''
    authorid = ''

    def __init__(self,bookid):
        self.bookid = str(bookid)
        self.get_book_info()
        self.get_chapterlist()

    def get_book_info(self):
        _bookinfo_api = 'http://android.jjwxc.net/androidapi/novelbasicinfo?novelId=' + bookid
        content = json.loads(self.s.get(_bookinfo_api).content)
        self.bookname = content['novelName']
        self.authorname = content['authorName']

    def get_chapterlist(self):
        _chaplist_api = 'http://android.jjwxc.net/androidapi/chapterList?novelId='+self.bookid+\
        '&offset=0&limit=1000&chapterserials=1'
        _chapdict = json.loads(self.s.get(_chaplist_api).content)
        for i in _chapdict['chapterlist']:
            if i['isvip'] != 0:
                self.vipchap_num += 1
            self._chap_list.append((i['chaptername']+i['chapterintro'],i['chapterid']))
        self.freechap_num = self.chapter_num-self.vipchap_num

    def get_singel_novel(self,chapterid):
        pass