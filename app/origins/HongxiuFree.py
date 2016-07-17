#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..logs import orilogger

#红袖添香站，origin_id = 2
class HongxiuFree:

    class_s = requests.session()
    bookname = ''
    bookid = ''
    authorname = ''
    authorid = ''
    status = ''
    _info_tuple = ()
    _chap_list = []
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    cover_url = ''

    def __init__(self, num):
        self.choose_book(num)
        self.bookname = self._info_tuple[0]
        self.bookid = str(self._info_tuple[1])
        self.get_book_info()
        #self.authorname = self._info_tuple[2]
        #self.authorid = str(self._info_tuple[3])
        self.status = self._info_tuple[2]
        self.get_chapterlist()

    def choose_book(self, num):
        if num > len(global_search_list)-1:
            orilogger.warning(u'红袖添香没有这么多符合要求的搜索，请重新选择。')
        self._info_tuple = global_search_list[num]

    def get_book_info(self):
        try:
            _bookinfo_api = 'http://novel.hongxiu.com/AndroidClient140401/book_cover_info/'+str(self.bookid)+'.json'
            res = json.loads(self.class_s.get(_bookinfo_api).content)
            self._authorname = res['response']['author']
            self._authorid = res['response']['aid']
            orilogger.info(u'正在获取\"'+self.bookname+u'\"书籍信息')
        except:
            orilogger.exception(u'获取\"'+self.bookname+u'\"失败！')

    def get_chapterlist(self):
        try:
            _chaplist_api = 'http://novel.hongxiu.com/AndroidClient140401/book_chapter_list/'+self.bookid+'.json'
            _chapdict = json.loads(self.class_s.get(_chaplist_api).content)
            for i in _chapdict['response']:
                if i['viptext'] == '0':
                    self.freechap_num += 1
                self._chap_list.append((i['title'],i['tid']))
            self.vipchap_num = self.chapter_num-self.freechap_num
        except:
            orilogger.exception(u'无法获取\"' + self.bookname + u'\"章节信息')

    def get_singel_novel(self, chapterid):
        try:
            _novel_api = 'http://novel.hongxiu.com/AndroidClient140401/book_chapter_get/'+self.bookid+'_'+chapterid+'.json'
            _novel = json.loads(self.class_s.get(_novel_api).content)['response'][chapterid]['chapter_content'].encode('utf-8')
            return _novel
        except:
            orilogger.exception(u'无法获取章节内容')
            return ''

    def generate_txt(self):
        try:
            file = open(r'app/data/txt/' + self.bookname + '.txt', 'w')
            file.write(self.bookname.encode('utf-8')+'\n'+u'由fanclley推送。'+'\n\n')
            for i in range(self.freechap_num):
                file.write(self._chap_list[i][0].encode('utf-8') + '\n\n' + self.get_singel_novel(
                    self._chap_list[i][1]) + '\n\n')
                orilogger.info(u'已写入' + self._chap_list[i][0])
            file.close()
        except:
            orilogger.exception(u'从起点中文网生成\"' + self.bookname + u'\"失败')

def keyword_search_Hongxiu(keyword):
    global global_search_list
    global_search_list = []
    local_s = requests.session()
    try:
        _searchapi = 'http://pad.hongxiu.com/aspxnovellist/androidclient/androidclientsearch.aspx?、' \
                     'method=store.search&kw='+keyword.encode('utf-8')+'&&order=mvote&&page=1&&per_page=10&'
        search_list = json.loads(local_s.get(_searchapi).content)
        for info in search_list['response']['data']:
            global_search_list.append(
                (info['title'], info['bid'], info['bookstatus']))
        if global_search_list == []:
            orilogger.warning(u'红袖添香未找到包含关键字\"' + keyword + u'\"的小说')
        return global_search_list
    except:
        orilogger.exception(u'无法获取红袖添香搜索结果')
        print 'oh'
        return global_search_list
#print keyword_search(u'医')
