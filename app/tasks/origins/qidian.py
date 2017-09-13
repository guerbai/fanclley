# -*- coding:utf-8 -*-
import json
import requests

#起点中文网。
class QidianFree(object):

    origin = u'起点'
    _book_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/GetChapterList?'\
        'BookId={bookid}'
    _chapter_api = 'http://4g.if.qidian.com/Atom.axd/Api/Book/'\
        'GetContent?BookId={bookid}&ChapterId={chapterid}'

    def get_cover_pic(self):
        pass

    def get_info(self, bookid):
        _book_api = self._book_api.format(bookid=bookid)
        res = requests.get(_book_api)
        content = res.content
        json_content = json.loads(content)
        authorname = json_content['Data']['Author']
        bookname = json_content['Data']['BookName']
        bookstatus = json_content['Data']['BookStatus']
        authorid = ''
        cover_url = ''
        buf = json_content['Data']['Chapters']
        # self.chapter_num = len(buf) - 1
        #第一章节总是版权声明，过滤掉。
        chapter_list = []
        for i in range(1, len(buf)):
            if not int(buf[i]['vc']) >= 80000:
                chapter_list.append((buf[i]['c'], str(buf[i]['n'])))
        return {
            'chapter_list': chapter_list,
            'bookname': bookname,
            'authorname': authorname,
            'authorid': authorid,
            'cover_url': cover_url,
            'bookstatus': bookstatus,
        }


    def get_singel_novel(self, bookid, chapterid):
        _chapter_api = self._chapter_api.format(
            bookid=bookid, chapterid=chapterid)
        res = requests.get(_chapter_api)
        content = res.content
        json_content = json.loads(content)
        novel_text = json_content['Data']
        return novel_text
