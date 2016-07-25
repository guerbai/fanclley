#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..loggers import orilogger
from antianti import USER_AGENTS,PROXIES
import random
import re
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

#起点中文网。
class QidianFree:

    #一本书是一个该类对象
    s = requests.session()
    s.headers['User-Agent'] = random.choice(USER_AGENTS)
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    _chap_list = []

    origin = u'起点'
    bookstatus = ''


    def __init__(self,bookid,bookname):

        self.bookid = bookid
        self.bookname = bookname
        #self.raw_url = raw_url

    def get_info(self):
        _chaplist_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId='+self.bookid
        try:
            _chapdict = json.loads(self.s.get(_chaplist_api,proxies=random.choice(PROXIES)).content)
            self.authorname = _chapdict['Data']['Author']
            buffer = _chapdict['Data']['Chapters']
            self.chapter_num = len(buffer) - 1
            #第一章节总是版权声明，过滤掉。
            for i in range(1, self.chapter_num + 1):
                if buffer[i]['vc'] >= '80000':
                    self.vipchap_num += 1
                self._chap_list.append((buffer[i]['n'], str(buffer[i]['c'])))
            self.freechap_num = self.chapter_num - self.vipchap_num
        except:
            orilogger.exception(u'连接'+_chaplist_api+u'出错！\n'+u'无法获取\"'+self.bookname+u'\"章节信息。')


    def get_singel_novel(self,chapterid):
        _novel_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetContent?BookId=' + self.bookid + '&ChapterId=' + chapterid
        try:
            _novel = json.loads(self.s.get(_novel_api,proxies=random.choice(PROXIES)).content)['Data']
            realnovel = str(_novel).replace(u'\r\n','    \n')
            # for i in str(_novel).split(u'\r\n'):
            #     realnovel += '    '+i+u'     \n'
            return realnovel
        except:
            orilogger.exception(u'无法获取'+_novel_api+u'的章节内容。')
            return ''

    def generate_txt(self):
        try:
            file = open(r'app/data/mobiworkshop/'+u'起点'+'_'+self.bookname + '.txt', 'w')
            file.write(r'% '+self.bookname+'\n'+r'% '+u'作者： '+self.authorname+'\n'+r'% '+u'由fanclley推送。'+'\n\n')
            orilogger.info(self.bookname+str(self.freechap_num)+u'免费章节')
            for i in range(self.freechap_num):
                file.write(r'# '+self._chap_list[i][0]+'\n\n'+self.get_singel_novel(self._chap_list[i][1])+'\n\n')
                orilogger.info(u'已写入' + self._chap_list[i][0])
            file.close()
        except:
            orilogger.exception(u'从起点中文网生成\"'+self.bookname+u'\.txt"失败')

    # def generate_md(self):
    #     try:
    #         file = open(r'app/data/mobiworkshop/'+u'起点'+'_'+self.bookname + '.md', 'w')
    #         #头信息。
    #         file.write(r'% '+self.bookname+'    \r\n'+'% '+u'作者： '+self.authorname\
    #                    +'    \r\n'+r'% '+u'\n由fanclley推送。'+'    \r\n')
    #         for i in range(self.freechap_num):
    #             anovel = self.get_singel_novel(self._chap_list[i][1])
    #             anovel.replace('\r\n','    \r\n')
    #             file.write('# ' + self._chap_list[i][0] + '    \r\n' + anovel + '    \r\n')
    #             orilogger.info(u'已写入' + self._chap_list[i][0])
    #         file.close()
    #     except:
    #         orilogger.exception(u'从起点中文网生成\"' + self.bookname + u'\.md"失败')



