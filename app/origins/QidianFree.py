#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json
from ..logs import orilogger

#起点中文网，origin_id = 1
class QidianFree:

    #一本书是一个该类对象
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

    def __init__(self,num):
        self.choose_book(num)
        self.bookname = self._info_tuple[0]
        self.bookid = str(self._info_tuple[1])
        self.authorname = self._info_tuple[2]
        self.authorid = str(self._info_tuple[3])
        self.status = self._info_tuple[4]
        self.get_chapterlist()

    def choose_book(self,num):
        if global_search_list == []:
            orilogger.warning(u'无书可选！')
        if num>len(global_search_list)-1:
            orilogger.warning(u'起点没有这么多符合要求的搜索，请重新选择。')
        self._info_tuple = global_search_list[num]


    def get_chapterlist(self):
        try:
            _chaplist_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=' + self.bookid
            _chapdict = json.loads(self.class_s.get(_chaplist_api).content)
            buffer = _chapdict['Data']['Chapters']
            self.chapter_num = len(buffer) - 1
            for i in range(1, self.chapter_num + 1):
                if buffer[i]['vc'] >= '80000':
                    self.vipchap_num += 1
                self._chap_list.append((buffer[i]['n'], str(buffer[i]['c'])))
            self.freechap_num = self.chapter_num - self.vipchap_num
            # print self.freechap_num
            # print self.vipchap_num
        except:
            orilogger.exception(u'无法获取\"'+self.bookname+u'\"章节信息')


    def get_singel_novel(self,chapterid):
        try:
            _novel_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetContent?BookId='+self.bookid+'&ChapterId='+chapterid
            _novel = json.loads(self.class_s.get(_novel_api).content)['Data'].encode('utf-8')
            return _novel
        except:
            orilogger.exception(u'无法获取章节内容')
            return ''

    def generate_txt(self):
        try:
            file = open(r'app/data/txt/'+self.bookname + '.txt', 'w')
            file.write(self.bookname.encode('utf-8')+'\n'+u'由fanclley推送。'.encode('utf-8')+'\n\n')
            orilogger.info(self.bookname+str(self.freechap_num)+u'免费章节')
            for i in range(self.freechap_num):
                file.write(self._chap_list[i][0].encode('utf-8')+'\n\n'+self.get_singel_novel(self._chap_list[i][1])+'\n\n')
                orilogger.info(u'已写入' + self._chap_list[i][0])
            file.close()
        except:
            orilogger.exception(u'从起点中文网生成\"'+self.bookname+u'\"失败')

def keyword_search_Qidian(keyword):
    global global_search_list
    global_search_list = []
    local_s = requests.session()
    try:
        _searchapi = 'http://4g.if.qidian.com/Atom.axd/Api/Search/AutoComplete?key=' + keyword.encode('utf-8')
        search_list = json.loads(local_s.get(_searchapi).content)
        for info in search_list['Data']:
            global_search_list.append(
                (info['BookName'], info['BookId'], info['AuthorName'], info['AuthorId'], info['BookStatus']))
        if global_search_list == []:
            orilogger.warning(u'起点中文网未找到包含关键字\"'+keyword+u'\"的小说')
        return global_search_list
    except:
        orilogger.exception(u'无法获取起点中文网搜索结果')
        return global_search_list

#print keyword_search(u'诛仙')
#a = QidianFree(0)
#print keyword_search(u'龙王传说')
#a = QidianFree(0)
#a.generate_txt()

