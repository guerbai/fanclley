#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Basebook:

    #一些基本信息，与数据库对应，可以为空。
    bookname = ''
    bookid = ''
    authorname = ''
    authorid = ''
    bookstatus = ''
    _info_tuple = ()
    _chap_list = []
    chapter_num = 0
    freechap_num = 0
    vipchap_num = 0
    cover_url = ''
    origin_id = 0
    raw_url = ''

    def __init__(self):
        pass

    def get_book_info(self):
        pass

    def get_chapterlist(self):
        pass

    def get_chapter_content(self):
        pass

    def generate_txt(self):
        pass

    def write_db(self):
        pass

