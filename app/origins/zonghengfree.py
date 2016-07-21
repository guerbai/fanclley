#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers  import orilogger
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")

#纵横中文网。
class zonghengfree:

    s = requests.session()
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    _chap_list = []
    bookname = ''
    bookid = ''
    bookstatus = ''
    authorname = ''
    params = '&brand=Xiaomi&channelId=A1007&channelType=H5&clientVersion=2.4.5.10&installId=5fd429ada47620979'\
             'cf1c8e63c3cb062&model=MI%2B3&modelName=pisces&operators=46002&os=android&osVersion=19&screenH='\
             '1920&screenW=1080&userId=0&sig=19a0de1a0e9a8583b6577a4c0cee8c6f'

    def __init__(self,bookid):
        self.bookid = bookid
        self.get_book_info()
        self.get_chapterlist()

    def get_book_info(self):
        _bookinfo_api = 'http://api1.zongheng.com/api/book/bookInfo?api_key=27A28A4D4B24022E543E&'\
                        'apn=wlan&appId=ZHKXS&bookId='+self.bookid+self.params
        try:
            _infodict = json.loads(self.s.get(_bookinfo_api).content)
            self.bookname = _infodict['result']['name']
            self.authorname = _infodict['result']['authorName']
        except:
            orilogger.exception(u'连接' + _bookinfo_api + u'出错！\n' + u'无法获取\"' + self.bookname + u'\"书籍信息。')

    def get_chapterlist(self):
        _chaplist_api = 'http://api1.zongheng.com/api/chapter/chapterList?api_key=27A28A4D4B24022E543E&'\
                        'apn=wlan&appId=ZHKXS&bookId='+self.bookid+self.params
        try:
            _chapdict = json.loads(self.s.get(_chaplist_api).content)
            for i in _chapdict['result']['chapterList']:
                self._chap_list.append((i['name'], str(i['chapterId'])))
                if i['isVip'] == 0:
                    self.freechap_num += 1
            self.chapter_num = len(self._chap_list)
            self.vipchap_num = self.chapter_num - self.freechap_num
        except:
            orilogger.exception(u'连接' + _chaplist_api + u'出错！\n' + u'无法获取\"' + self.bookname + u'\"章节信息。')

    def get_singel_novel(self, chapterid):
        url = 'http://book.zongheng.com/chapter/'+self.bookid+'/'+chapterid+'.html'
        _novel = u''
        try:
            res = self.s.get(url).content
            soup = BeautifulSoup(res, 'lxml')
            wrap = soup.find('div', class_='content')
            buffer = wrap.find_all('p')
            for i in range(len(buffer) - 5):
                _novel += '  '+buffer[i].text
            return _novel
        except:
            orilogger.exception(u'无法获取' + url + u'的章节内容。')
            return ''

    def generate_txt(self):
        file = open(r'app/data/txt/' + u'纵横' + '_' + self.bookid + '.txt', 'w')
        try:
            file.write(self.bookname + '\n' + u'作者： ' + self.authorname + u'\n由fanclley推送。' + '\n\n')
            orilogger.info(self.bookname + str(self.freechap_num) + u'免费章节')
            for i in range(self.freechap_num):
                file.write(self._chap_list[i][0] + '\n\n' + self.get_singel_novel(self._chap_list[i][1]) + '\n\n')
                orilogger.info(u'已写入' + self._chap_list[i][0])

        except:
            orilogger.exception(u'从纵横中文网生成\"' + self.bookname + u'\.txt"失败')

