# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash,jsonify
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm
from .. import db
from forms import SearchForm
from ..taskhandler import hardtask
from ..origins import Search


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

@main.route('/downloadfree/<origin>/<bookid>/<bookname>')
def downloadfree(origin,bookid,bookname):

    if current_user.kindle_loc == None:
        flash(u'请先填写你的kindle邮箱，并把服务邮箱加入到你的kindle信任邮箱中。')
    else:
        #print abook
        #print type(abook)
        hardtask.delay(current_user.kindle_loc,origin,bookid,bookname)
        flash(u'你的推送已加入任务队列，请注意查收。')
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

