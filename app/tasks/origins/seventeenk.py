# -*- coding:utf-8 -*-
import json
import requests

#17k小说站。
class SeventeenkFree(object):

    origin = u'17K'
    _chaplist_api = 'http://client1.17k.com/rest/download/'\
        'getBookVolumeSimpleListBybid?bookId={bookid}'\
        '&tokenId=aGQxZWo2MkA6MTMxMTcyOTI5MToyMDAxMDY3'
    _info_api = 'http://client1.17k.com/rest/bookintroduction/getBookByid?'\
        'bookId={bookid}'
    _chapter_api = 'http://client1.17k.com/rest/download/downChapterV2?'\
        'chapterId={chapterid}&tokenId=aGQxZWo2MkA6MTMxMTcyOTI5MToyMDAxMDY3'

    def get_info(self, bookid):
        _info_api = self._info_api.format(bookid=bookid)
        res = requests.get(_info_api)
        content = res.content
        info_content = json.loads(content)

        _chaplist_api = self._chaplist_api.format(bookid=bookid)
        cl_res = requests.get(_chaplist_api)
        content = cl_res.content
        chapterlist_content = json.loads(content)

        bookname = info_content['book']['bookName']
        authorname = info_content['book']['authorPenname']
        authorid = info_content['book']['authorId']
        cover_url = info_content['book']['coverImageUrl']
        bookstatus = info_content['book']['bookstatus']

        chapter_list = []
        for i in chapterlist_content['volumeList']:
            if i['name'] == '作品相关':
                continue
            for j in i['chapterList']:
                if j['isFree'] == 'true':
                    chapter_list.append((j['id'],j['name']))
        return {
            'chapter_list': chapter_list,
            'bookname': bookname,
            'authorname': authorname,
            'authorid': authorid,
            'cover_url': cover_url,
            'bookstatus': bookstatus,
        }

    def get_singel_novel(self, bookid, chapterid):
        _chapter_api = self._chapter_api.format(chapterid=chapterid)
        res = requests.get(_chapter_api)
        content = res.content
        json_content = json.loads(content)
        novel_text = json_content['content']
        return novel_text
