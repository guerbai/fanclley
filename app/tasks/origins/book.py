# -*- coding:utf-8 -*-
from __init__ import origin_table
from qidian import QidianFree
# from . import book_origins

class Book(object):

    def __init__(self, origin, bookid):
        self.origin = origin_table[origin]()
        self.bookid = bookid
        info = self.origin.get_info(self.bookid)
        self.bookname = info['bookname']
        self.raw_url = ''
        self.bookstatus = info['bookstatus']
        self.cover_url = info['cover_url']
        self.authorname = info['authorname']
        self.authorid = info['authorid']
        # (chapter_id, chapter_name)
        self.chapter_list = info['chapter_list']
        self.content = {}

    def get_content(self):
        content = {}
        for chapter in self.chapter_list:
            chapter_id = chapter[0]
            chapter_name = chapter[1]
            chapter_text = self.origin.get_singel_novel(self.bookid, chapter_id)
            content[chapter_name] = chapter_text
        self.content = content

    def generate_txt(self):
        self.get_content()
        with open('test.txt', 'w') as f:
            for k in self.content:
                f.write(k)
                f.write('\n')
                f.write(self.content[k])
                f.write('\n==========================\n')
        print ('ok ya!')

if __name__ == '__main__':
    book = Book('qidian', '1009838140')
    book.generate_txt()
