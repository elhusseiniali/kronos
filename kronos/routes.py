from flask import render_template, flash, redirect, url_for, request
from kronos import app, db, bcrypt, api
from kronos.forms import RegistrationForm, LoginForm
from kronos.models import User, Monster, MonsterEffect, State
from kronos.models import BoardMonster, BoardMonsterEffect
from kronos.models import Game, Board

from flask_login import login_user, current_user, logout_user, login_required

from flask_restplus import Resource

import random


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register",
           methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/login",
           methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page \
                else redirect(url_for('home'))
        else:
            flash("Login unsuccessful!", 'danger')

    return render_template('login.html',
                           title='Log in',
                           form=form)


@app.route("/logout",
           methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html',
                           title='Account')


@api.route('/user/id=<int:id>',
           doc={'description': 'Get User stats from user id.'})
@api.doc(params={'id': 'User ID'})
class GetUserStats(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {
            'id': id,
            'username': user.username,
            'email': user.email,
            'wins': user.win,
            'losses': user.loss,
            'ties': user.tie
        }


@api.route('/user/board/id=<int:id>',
           doc={'description': 'Get all user boards from user id.'})
@api.doc(params={'id': 'User ID'})
class GetUserBoards(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {
            i: user.boards[i].id for i in range(0, len(user.boards))
        }


@api.route('/monster/id=<int:id>',
           doc={'description': 'Get monster name and attributes from id.'})
@api.doc(params={'id': 'Monster ID'})
class GetMonsterStats(Resource):
    def get(self, id):
        monster = Monster.query.filter_by(id=id).first()
        return {
            'id': id,
            'name': monster.name,
            'attack': monster.attack_points,
            'defense': monster.defense_points
        }
