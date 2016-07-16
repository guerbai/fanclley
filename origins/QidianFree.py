#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests,json

s = requests.session()
class QidianFree:

    #一本书是一个该类对象



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
        self._info_tuple = global_search_list[num]


    def get_chapterlist(self):
        _chaplist_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?BookId=' + self.bookid
        _chapdict = json.loads(s.get(_chaplist_api).content)
        buffer = _chapdict['Data']['Chapters']
        self.chapter_num = len(buffer)-1
        for i in range(1,self.chapter_num+1):
            if buffer[i]['vc'] != '80000':
                self.freechap_num += 1
            self._chap_list.append((buffer[i]['n'], str(buffer[i]['c'])))
        self.vipchap_num = self.chapter_num-self.freechap_num
        print self.freechap_num
        print self.vipchap_num


    def get_singel_novel(self,chapterid):
        #chapterid = self._chap_list[num]
        _novel_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetContent?BookId='+self.bookid+'&ChapterId='+chapterid
        _novel = json.loads(s.get(_novel_api).content)['Data'].encode('utf-8')
        #print _novel
        return _novel

    def generate_txt(self):
        file = open(r'/home/fyb/codes/fanclley/app/data/'+self.bookname + '.txt', 'w')
        print self.freechap_num
        for i in range(self.freechap_num):
            print u'写入'+self._chap_list[i][0]
            file.write(self._chap_list[i][0].encode('utf-8')+'\n\n'+self.get_singel_novel(self._chap_list[i][1])+'\n\n')
        file.close()


def keyword_search(keyword):
    global global_search_list
    global_search_list = []
    _searchapi = 'http://4g.if.qidian.com/Atom.axd/Api/Search/AutoComplete?key=' + keyword
    search_list = json.loads(s.get(_searchapi).content)
    for info in search_list['Data']:
        global_search_list.append(
            (info['BookName'], info['BookId'], info['AuthorName'], info['AuthorId'], info['BookStatus']))
    return global_search_list


#print keyword_search(u'诛仙')
#a = QidianFree(0)
#print keyword_search(u'龙王传说')
#a = QidianFree(0)
#a.generate_txt()

