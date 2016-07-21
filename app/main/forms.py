# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User


class SearchForm(Form):
    keyword = StringField(u'请输入书名或关键字查询：', validators=[Required()])
    submit = SubmitField(u'搜索')


class EditProfileForm(Form):
    kindle_loc = StringField(u'kindle推送邮箱：', validators=[Length(0, 64),Email()])
    qidian_login = StringField(u'起点中文网登录帐号：')#, validators=[Length(0, 64),Email()])
    qidian_password = StringField(u'起点中文网登录密码：')#, validators=[Length(0, 64)])
    hongxiu_login = StringField(u'红袖添香登录帐号：')#, validators=[Length(0, 64),Email()])
    hongxiu_password = StringField(u'红袖添香登录密码：')#, validators=[Length(0, 64)])
    submit = SubmitField(u'保存')


