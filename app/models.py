# -*- coding:utf-8 -*-
from . import db

class Origin(db.Model):
    __tablename__ = 'origins'
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.Unicode,unique=True)
    books = db.relationship('Book',backref='origin')

    def __repr__(self):
        return '<Origin %r>' % self.name

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.Unicode)
    bookid = db.Column(db.BigInteger)
    authorname = db.Column(db.Unicode)
    authorid = db.Column(db.BigInteger)
    status = db.Column(db.Unicode)
    chapter_num = db.Column(db.Integer)
    freechap_num = db.Column(db.Integer)
    vipchap_num = db.Column(db.Integer)
    cover_url = db.Column(db.Unicode)
    raw_url = db.Column(db.String)
    origin_id = db.Column(db.SmallInteger, db.ForeignKey('origins.id'))
    chapters = db.relationship('Chapter',backref='Book')

    def __init__(self,origin_id):
        self.origin_id = origin_id

    def __repr__(self):
        return '<Book %r>' % self.name

# only free chapters
class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.BigInteger, primary_key=True)
    chapterid = db.Column(db.BigInteger)
    chaptername = db.Column(db.Unicode)
    chapter_content = db.Column(db.UnicodeText)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    def __init__(self,book_id):
        self.book_id = book_id

    def __repr__(self):
        return '<Chapter %r>' % self.name

