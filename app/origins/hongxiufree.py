#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers  import orilogger
import sys
import re
reload(sys)
sys.setdefaultencoding("utf-8")

#红袖添香站。
class HongxiuFree:

    s = requests.session()
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    _chap_list = []

    origin = u'红袖'
    bookstatus = ''

    def __init__(self, bookid, bookname):
        self.bookid = bookid
        self.bookname = bookname
        #self.raw_url = raw_url


    def get_info(self):
        try:
            pattern = re.compile(r'title":"(.*?)","bookstatus":.*?author":"(.*?)"', re.S)
            _bookinfo_api = 'http://novel.hongxiu.com/AndroidClient140401/book_cover_info/' + self.bookid + '.json'
            res = self.s.get(_bookinfo_api).content
            items = re.findall(pattern, res)
            for item in items:
                self.authorname = item[1]
            self.get_chapterlist()
            orilogger.info(u'已获取\"' + self.bookname + u'\"书籍信息')
        except:
            orilogger.exception(u'于红袖添香获取信息失败！')

    def get_chapterlist(self):
        _chaplist_api = 'http://novel.hongxiu.com/AndroidClient140401/book_chapter_list/'+self.bookid+'.json'
        try:
            _chapdict = json.loads(self.s.get(_chaplist_api).content)
            for i in _chapdict['response']:
                if i['viptext'] == '0':
                    self.freechap_num += 1
                self._chap_list.append((i['title'],i['tid']))
            self.vipchap_num = self.chapter_num-self.freechap_num
        except:
            orilogger.exception(u'连接'+_chaplist_api+u'出错！\n'+u'无法获取\"'+self.bookname+u'\"章节信息。')

    def get_singel_novel(self, chapterid):
        _novel_api = 'http://novel.hongxiu.com/AndroidClient140401/book_chapter_get/' + self.bookid + '_' + chapterid + '.json'
        try:
            _novel_api = 'http://novel.hongxiu.com/AndroidClient140401/book_chapter_get/'+self.bookid+'_'+chapterid+'.json'
            _novel = json.loads(self.s.get(_novel_api).content)['response'][chapterid]['chapter_content']
            return _novel
        except:
            orilogger.exception(u'无法获取'+_novel_api+u'的章节内容。')
            return ''

    def generate_txt(self):
        try:
            file = open(r'app/data/txt/' + u'红袖'+'_'+self.bookname + '.txt', 'w')
            file.write(r'% '+self.bookname+'\n'+r'% '+u'作者： '+self.authorname+r'% '+u'\n由fanclley推送。'+'\n\n')
            for i in range(self.freechap_num):
                file.write('# '+self._chap_list[i][0] + '\n\n' + self.get_singel_novel(self._chap_list[i][1]) + '\n\n')
                orilogger.info(u'已写入' + self._chap_list[i][0])
            file.close()
        except:
            orilogger.exception(u'从红袖添香网生成txt电子书失败！')



