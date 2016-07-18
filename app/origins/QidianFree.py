#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..logs import orilogger
from . import basebook

#起点中文网，origin_id = 1
class QidianFree(basebook):

    #一本书是一个该类对象
    origin_id = 1

    def __init__(self,atuple):
        self.bookname = atuple[0].encode('utf-8')
        self.bookid = str(atuple[1])
        self.authorname = atuple[2].encode('utf-8')
        self.authorid = str(atuple[3])
        self.bookstatus = atuple[4]
        self.raw_url = atuple[5]
        self.get_chapterlist()

    def get_chapterlist(self):
        _chaplist_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=' + self.bookid
        try:
            _chapdict = json.loads(self.s.get(_chaplist_api).content)
            buffer = _chapdict['Data']['Chapters']
            self.chapter_num = len(buffer) - 1
            #第一章节总是版权声明，过滤掉。
            for i in range(1, self.chapter_num + 1):
                if buffer[i]['vc'] >= '80000':
                    self.vipchap_num += 1
                self._chap_list.append((buffer[i]['n'].encode('utf-8'), str(buffer[i]['c'])))
            self.freechap_num = self.chapter_num - self.vipchap_num
        except:
            orilogger.exception(u'连接'+_chaplist_api+u'出错！\n'+u'无法获取\"'+self.bookname+u'\"章节信息。')


    def get_singel_novel(self,chapterid):
        _novel_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetContent?BookId=' + self.bookid + '&ChapterId=' + chapterid
        try:
            _novel = json.loads(self.class_s.get(_novel_api).content)['Data'].encode('utf-8')
            return _novel
        except:
            orilogger.exception(u'无法获取'+_novel_api+u'的章节内容。')
            return ''

    def generate_txt(self):
        try:
            file = open(r'app/data/txt/'+self.bookname + '.txt', 'w')
            file.write(self.bookname+'\n'+u'作者： '+self.authorname+u'\n由fanclley推送。'+'\n\n')
            orilogger.info(self.bookname+str(self.freechap_num)+u'免费章节')
            for i in range(self.freechap_num):
                file.write(self._chap_list[i][0]+'\n\n'+self.get_singel_novel(self._chap_list[i][1])+'\n\n')
                orilogger.info(u'已写入' + self._chap_list[i][0])
            file.close()
            self.write_db()
        except:
            orilogger.exception(u'从起点中文网生成\"'+self.bookname+u'\.txt"失败')

    def write_db(self):
        pass

