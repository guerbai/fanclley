# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class SearchForm(Form):
    keyword = StringField(u'请输入书名或关键字查询：', validators=[Required()])
    submit = SubmitField(u'搜索')


class EditProfileForm(Form):
    kindle_loc = StringField(u'kindle推送邮箱：', validators=[Length(0, 64)])
    qidian_login = StringField(u'起点中文网登录帐号：', validators=[Length(0, 64)])
    qidian_password = StringField(u'起点中文网登录密码：', validators=[Length(0, 64)])
    hongxiu_login = StringField(u'红袖添香登录帐号：', validators=[Length(0, 64)])
    hongxiu_password = StringField(u'红袖添香登录密码：', validators=[Length(0, 64)])

    submit = SubmitField(u'保存')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
