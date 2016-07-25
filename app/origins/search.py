#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers import orilogger
from .basebook import Basebook
from bs4 import BeautifulSoup
from antianti import USER_AGENTS,PROXIES
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Search:

    s = requests.session()
    s.headers['User-Agent'] = random.choice(USER_AGENTS)
    qidian_num = 0
    hongxiu_num = 0

    def __init__(self,keyword):
        self.keyword = keyword
        self.search_handler()

    #处理调用搜索网站顺序。
    def search_handler(self):
        self.res_list = []
        self.search_Qidian()
        self.search_Hongxiu()
        self.search_17k()
        self.search_zongheng()

    def search_Qidian(self):
        _searchapi = 'http://4g.if.qidian.com/Atom.axd/Api/Search/AutoComplete?key=' + self.keyword
        myres = []
        try:
            search_list = json.loads(self.s.get(_searchapi,proxies=random.choice(PROXIES)).content)
            for info in search_list['Data']:
                if info['Type'] != 'book':
                    continue
                abook = Basebook()
                abook.origin = u'起点'
                abook.bookname = info['BookName']
                abook.bookid = str(info['BookId'])
                #abook.bookstatus = info['BookStatus']
                abook.authorname = info['AuthorName']
                abook.raw_url = 'http://www.qidian.com/Book/'+str(info['BookId'])+'.aspx'
                myres.append(abook)
            if len(myres)>5:
                myres = myres[:5]
            self.res_list+=myres
            if myres == []:
                orilogger.info(u'起点中文网未找到包含关键字\"' + self.keyword + u'\"的小说')
            return myres
        except:
            orilogger.exception(u'无法连接'+_searchapi+u',\n无法获取起点中文网搜索结果。')
            return myres

    def search_Hongxiu(self):
        _searchapi = 'http://pad.hongxiu.com/aspxnovellist/androidclient/androidclientsearch.aspx?'\
                     'method=store.search&kw=' + self.keyword + '&&order=mvote&&page=1&&per_page=5&'
        myres = []
        try:
            search_list = json.loads(self.s.get(_searchapi,proxies=random.choice(PROXIES)).content)
            for info in search_list['response']['data']:
                abook = Basebook()
                abook.origin = u'红袖'
                abook.bookname = info['title']
                abook.bookid = str(info['bid'])
                #abook.bookstatus = info['bookstatus']
                abook.raw_url = 'http://novel.hongxiu.com/a/'+str(info['bid'])+'/'
                myres.append(abook)
            self.res_list+=myres
            if myres == []:
                orilogger.info(u'红袖添香未找到包含关键字\"' + self.keyword + u'\"的小说')
            return myres
        except:
            orilogger.exception(u'无法连接'+_searchapi+u',\n无法获取红袖添香搜索结果。')
            return myres


    def search_17k(self):
        _searchapi = 'http://search.17k.com/h5/sl?q='+self.keyword+'&page=0&pageSize=5'
        myres = []
        try:
            search_list = json.loads(self.s.get(_searchapi,proxies=random.choice(PROXIES)).content)
            for info in search_list['viewList']:
                abook = Basebook()
                abook.origin = u'17K'
                abook.bookname = info['bookName']
                abook.bookid = str(info['bookId'])
                abook.authorname = info['authorPenname']
                #abook.bookstatus = info['bookStatus']
                abook.raw_url = 'http://www.17k.com/list/'+abook.bookid+'.html'
                myres.append(abook)
            self.res_list+=myres
            if myres == []:
                orilogger.info(u'17K未找到包含关键字\"' + self.keyword + u'\"的小说')
            return myres
        except:
            orilogger.exception(u'无法连接' + _searchapi + u',\n无法获取17K搜索结果。')
            return myres

    def search_zongheng(self):
        url = 'http://search.zongheng.com/search/all/' + self.keyword + '/1.html'
        myres = []
        try:
            res = self.s.get(url,proxies=random.choice(PROXIES)).text
            soup = BeautifulSoup(res, 'lxml')
            div = soup.find_all('div', class_='search_text')
            if len(div) > 5:
                div = div[:5]
            for i in div:
                abook = Basebook()
                abook.origin = u'纵横'
                abook.bookname = i.find('h2').find('a').text
                abook.raw_url = i.find('h2').find('a')['href']
                abook.bookid = str(abook.raw_url.split('/')[-1].split('.')[0])
                myres.append(abook)
            self.res_list+=myres
            if myres == []:
                orilogger.info(u'纵横中文网未找到包含关键字\"' + self.keyword + u'\"的小说')
            return myres
        except:
            orilogger.exception(u'无法连接' + url + u',\n无法获取纵横搜索结果。')
            return myres


