#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..logs import orilogger

class search:

    s = requests.session()

    def __init__(self,keyword):
        self.keyword = keyword.encode('utf-8')
        self.res_list = []
        self.search_handler()

    #处理调用搜索网站顺序。
    def search_handler(self):
        self.search_Qidian()
        self.search_Hongxiu()

    def search_Qidian(self):
        _searchapi = 'http://4g.if.qidian.com/Atom.axd/Api/Search/AutoComplete?key=' + self.keyword
        try:

            search_list = json.loads(self.s.get(_searchapi).content)
            for info in search_list['Data']:
                raw_url = 'http://www.qidian.com/Book/'+str(info['BookId'])+'.aspx'
                self.res_list.append(
                    (info['BookName'],info['BookId'],info['AuthorName'],info['AuthorId'],info['BookStatus'],raw_url))
            if self.res_list == []:
                orilogger.warning(u'起点中文网未找到包含关键字\"' + self.keyword + u'\"的小说')
            return self.res_list
        except:
            orilogger.exception(u'无法连接'+_searchapi+u',\n无法获取起点中文网搜索结果。')
            return self.res_list

    def search_Hongxiu(self):
        _searchapi = 'http://pad.hongxiu.com/aspxnovellist/androidclient/androidclientsearch.aspx?、' \
                     'method=store.search&kw=' + self.keyword + '&&order=mvote&&page=1&&per_page=10&'
        try:
            search_list = json.loads(self.s.get(_searchapi).content)
            for info in search_list['response']['data']:
                raw_url = 'http://novel.hongxiu.com/a/'+str(info['bid'])+'/'
                self.res_list.append(
                    (info['title'], info['bid'], info['bookstatus'],raw_url))
            if self.res_list == []:
                orilogger.warning(u'红袖添香未找到包含关键字\"' + self.keyword + u'\"的小说')
            return self.res_list
        except:
            orilogger.exception(u'无法连接'+_searchapi+u',\n无法获取红袖添香搜索结果。')
            return self.res_list


