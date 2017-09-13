# -*- coding: utf-8 -*-
from origin import *

origin_table = {
	'qidian': QidianFree,
	'hongxiu': HongxiuFree,
	'17k': SeventeenkFree,
	'zongheng': ZonghengFree,
}

workshop_dir = '../../../mobi_workshop'

def build_book(origin, bookid):
	book_text = origin_table[origin](bookid).construct_text()

