#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers  import orilogger
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

#纵横中文网。
class Zonghengfree:

    s = requests.session()
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    _chap_list = []

    origin = u'纵横'
    bookstatus = ''

    def __init__(self, bookid, bookname):

        self.bookid = bookid
        self.bookname = bookname
        #self.raw_url = raw_url

    def get_info(self):
        url = 'http://book.zongheng.com/showchapter/'+self.bookid+'.html'
        try:
            res = self.s.get(url).text
            soup = BeautifulSoup(res, 'lxml')
            self.authorname = soup.find('div', class_='tc txt').find('a').text
            buffer = soup.find_all('td', class_='chapterBean')
            self.chapter_num = len(buffer)
            for i in buffer:
                if not i.find('em'):
                    self.freechap_num += 1
                chaptername = i.find('a').text
                chapterid = str(i.find('a')['href'].split('/')[-1].split('.')[0])
                self._chap_list.append((chaptername, chapterid))
            self.vipchap_num = self.chapter_num-self.freechap_num
            orilogger.info(u'已获取\"'+self.bookname+u'\"信息。')
        except:
            orilogger.exception(u'连接或解析' + url + u'出错！\n' + u'无法获取书籍章节信息。')

    def get_singel_novel(self, chapterid):
        url = 'http://book.zongheng.com/chapter/'+self.bookid+'/'+chapterid+'.html'
        _novel = u''
        try:
            res = self.s.get(url).content
            soup = BeautifulSoup(res, 'lxml')
            wrap = soup.find('div', class_='content')
            buffer = wrap.find_all('p')
            for i in range(len(buffer) - 5):
                _novel += '    '+buffer[i].text+'\n'
            return _novel
        except:
            orilogger.exception(u'无法获取' + url + u'的章节内容。')
            return ''

    def generate_txt(self):
        file = open(r'app/data/txt/' + u'纵横' + '_' + self.bookname + '.txt', 'w')
        try:
            file.write(r'% '+self.bookname+'\n'+r'% '+u'作者： '+self.authorname+r'% '+u'\n由fanclley推送。'+'\n\n')
            orilogger.info(self.bookname + str(self.freechap_num) + u'免费章节')
            for i in range(self.freechap_num):
                file.write('# '+self._chap_list[i][0] + '\n\n' + self.get_singel_novel(self._chap_list[i][1]) + '\n\n')
                orilogger.info(u'已写入' + self._chap_list[i][0])

        except:
            orilogger.exception(u'从纵横中文网生成\"' + self.bookname + u'\.txt"失败')

