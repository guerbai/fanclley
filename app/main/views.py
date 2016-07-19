# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Role, User
from ..decorators import admin_required
from forms import SearchForm


@main.route('/',methods=['GET', 'POST'])
def index():
    form = SearchForm()
    '''if form.validate_on_submit():
        keyword = form.keyword.data
        return redirect((url_for('.searh_res',keyword=keyword)))'''
    return render_template('index.html',form=form)

'''@main.route('/')
def search_res():
    return render_template('index.html')'''

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.kindle_loc = form.kindle_loc.data
        current_user.qidian_login = form.qidian_login
        current_user.qidian_password = form.qidian_password
        current_user.hongxiu_login = form.hongxiu_login
        current_user.hongxiu_password = form.hongxiu_password
        db.session.add(current_user)
        flash(u'你的信息已更新.')
        return redirect(url_for('.edit_profile', username=current_user.username))
    form.kindle_loc.data = current_user.kindle_loc
    form.qidian_login.data = current_user.qidian_login
    form.qidian_password.data = current_user.qidian_password
    form.hongxiu_login.data = current_user.hongxiu_login
    form.hongxiu_password.data = current_user.hongxiu_password
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    return render_template('edit_profile.html', form=form, user=user)
