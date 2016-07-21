#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers import orilogger
from .basebook import Basebook
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Search:

    s = requests.session()
    qidian_num = 0
    hongxiu_num = 0

    def __init__(self,keyword):
        self.keyword = keyword
        self.search_handler()

    #处理调用搜索网站顺序。
    def search_handler(self):
        self.res_list = []
        self.search_Qidian()
        if len(self.res_list)>5:
            self.res_list = self.res_list[:5]
        self.qidian_num = len(self.res_list)
        self.search_Hongxiu()
        self.hongxiu_num = len(self.res_list)-self.qidian_num
        self.search_17k()

    def search_Qidian(self):
        _searchapi = 'http://4g.if.qidian.com/Atom.axd/Api/Search/AutoComplete?key=' + self.keyword
        try:
            search_list = json.loads(self.s.get(_searchapi).content)
            for info in search_list['Data']:
                if info['Type'] != 'book':
                    continue
                abook = Basebook()
                abook.origin = u'起点'
                abook.bookname = info['BookName']
                abook.bookid = str(info['BookId'])
                abook.bookstatus = info['BookStatus']
                abook.raw_url = 'http://www.qidian.com/Book/'+str(info['BookId'])+'.aspx'
                self.res_list.append(abook)
            if self.res_list == []:
                orilogger.info(u'起点中文网未找到包含关键字\"' + self.keyword + u'\"的小说')
            return self.res_list
        except:
            orilogger.exception(u'无法连接'+_searchapi+u',\n无法获取起点中文网搜索结果。')
            return self.res_list

    def search_Hongxiu(self):
        _searchapi = 'http://pad.hongxiu.com/aspxnovellist/androidclient/androidclientsearch.aspx?'\
                     'method=store.search&kw=' + self.keyword + '&&order=mvote&&page=1&&per_page=5&'
        try:
            search_list = json.loads(self.s.get(_searchapi).content)
            for info in search_list['response']['data']:
                abook = Basebook()
                abook.origin = u'红袖'
                abook.bookname = info['title']
                abook.bookid = str(info['bid'])
                abook.bookstatus = info['bookstatus']
                abook.raw_url = 'http://novel.hongxiu.com/a/'+str(info['bid'])+'/'
                self.res_list.append(abook)
            if self.res_list == []:
                orilogger.info(u'红袖添香未找到包含关键字\"' + self.keyword + u'\"的小说')
            return self.res_list
        except:
            orilogger.exception(u'无法连接'+_searchapi+u',\n无法获取红袖添香搜索结果。')
            return self.res_list


    def search_17k(self):
        _searchapi = 'http://search.17k.com/h5/sl?q='+self.keyword+'&page=0&pageSize=5'
        try:
            search_list = json.loads(self.s.get(_searchapi).content)
            for info in search_list['viewList']:
                abook = Basebook()
                abook.origin = u'17K'
                abook.bookname = info['bookName']
                abook.bookid = str(info['bookId'])
                abook.bookstatus = info['bookStatus']
                abook.raw_url = 'http://www.17k.com/list/'+abook.bookid+'.html'
                self.res_list.append(abook)
            if self.res_list == []:
                orilogger.info(u'17K未找到包含关键字\"' + self.keyword + u'\"的小说')
            return self.res_list
        except:
            orilogger.exception(u'无法连接' + _searchapi + u',\n无法获取17K搜索结果。')
            return self.res_list

    def search_zongheng(self):
        _searchapi = 'http://api1.zongheng.com/api/search/book?userId=0&installId=5fd429ada47620979cf1c8e63c3cb062'\
                     '&modelName=pisces&osVersion=19&api_key=27A28A4D4B24022E543E&operators=46002&clientVersion='\
                     '2.4.5.10&os=android&appId=ZHKXS&key='+self.keyword+'&apn=wlan&screenH=1920&page=0&channelId'\
                     '=A1007&model=MI+3&type=all&brand=Xiaomi&sig=357b1e6a2ab3cbcc7a85f819477ed74c&channelType=H5'\
                     '&size=0&screenW=1080'
        try:
            search_list = json.loads(self.s.get(_searchapi).content)
            for info in search_list['result']['bookList']:
                abook = Basebook()
                abook.origin = u'纵横'
                abook.bookname = info['name']
                abook.bookid = str(info['bookId'])
                abook.bookstatus = info['bookStatus']
                abook.raw_url = 'http://www.17k.com/list/' + abook.bookid + '.html'
                self.res_list.append(abook)
            if self.res_list == []:
                orilogger.info(u'17K未找到包含关键字\"' + self.keyword + u'\"的小说')
            return self.res_list

        except:
            orilogger.exception(u'无法连接' + _searchapi + u',\n无法获取17K搜索结果。')
            return self.res_list
