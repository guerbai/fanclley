# -*- coding: utf-8 -*-
import requests
from _book import Basebook
from _proxy import USER_AGENTS, PROXIES


class Origin(object):

    s = requests.session()

    def __init__(self, bookid):
        self.book = Basebook('qidian', bookid)

    @staticmethod
    def get_header():
        return random.choice(USER_AGENTS)

    def get_cover_pic(self):
        raise NotImplementErro('Implement this func!')

    def get_info(self):
        raise NotImplementErro('Implement this func!')

    def get_chapter_list(self):
        raise NotImplementErro('Implement this func!')

    def get_single_chapter(self, chapterid):
        raise NotImplementErro('Implement this func!')

    def construct_text(self):
        raise NotImplementErro('Implement this func!')
