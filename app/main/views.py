# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm
from .. import db
from forms import SearchForm
from ..origins import Search,QidianFree,HongxiuFree,seventeenfree
from ..sendemail import sendto_kindle


@main.route('/',methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.keyword.data
        #res_list = Search(keyword).res_list
        return redirect(url_for('.search_res',keyword=keyword))
    return render_template('index.html',form=form)

@main.route('/search_res/<keyword>',methods=['GET', 'POST'])
def search_res(keyword=None):
    if keyword != None:
        res_list = Search(keyword).res_list
        return render_template('search_res.html',result = res_list)
    else:
        return redirect(url_for('.index'))

@main.route('/downloadfree/<origin>/<bookid>')
def downloadfree(origin='',bookid=None):
    if bookid != None:
        if origin == u'起点':
            QidianFree(bookid).generate_txt()
        if origin == u'红袖':
            HongxiuFree(bookid).generate_txt()
        if origin == u'17K':
            seventeenfree(bookid).generate_txt()
    else:
        flash(u'发送失败。')
        return redirect(url_for('.index'))
    if current_user.kindle_loc == None:
        flash(u'请填写你的kindle邮箱，并把服务邮箱加入到你的kindle信任邮箱中。')
        return redirect(url_for('.index'))
    sendto_kindle(current_user.kindle_loc,origin+'_'+str(bookid))
    flash(u'发送成功，请注意查收！')
    return redirect(url_for('.index'))

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.kindle_loc = form.kindle_loc.data
        current_user.qidian_login = form.qidian_login.data
        current_user.qidian_password = form.qidian_password.data
        current_user.hongxiu_login = form.hongxiu_login.data
        current_user.hongxiu_password = form.hongxiu_password.data
        db.session.add(current_user)
        #db.session.commit()
        flash(u'你的信息已更新.')
        return redirect(url_for('.index'))
    form.kindle_loc.data = current_user.kindle_loc
    form.qidian_login.data = current_user.qidian_login
    form.qidian_password.data = current_user.qidian_password
    form.hongxiu_login.data = current_user.hongxiu_login
    form.hongxiu_password.data = current_user.hongxiu_password
    return render_template('edit_profile.html', form=form)

