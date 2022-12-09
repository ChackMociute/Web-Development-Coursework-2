from app import app, db, admin, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user
from .models import User, Artist, Album, Song
from .forms import LoginForm


from random import choice, choices, seed
from datetime import date
from time import mktime

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Artist, db.session))
admin.add_view(ModelView(Album, db.session))
admin.add_view(ModelView(Song, db.session))


def base(page, **kwargs):
    if 'login' in request.form:
        return redirect(url_for('login'))
    if 'signup' in request.form:
        return redirect(url_for('signup'))
    if 'logout' in request.form:
        logout_user()
    return render_template(f"{page}.html", **kwargs)

def recommendations():
    seed(mktime(date.today().timetuple()))
    artists = choices(Artist.query.all(), k=3)
    albums = [choice(artist.albums) for artist in artists]
    songs = [choice(album.songs) for album in albums]
    return [
        {'artist': artist, 'song': song, 'album': album}
        for artist, album, song
        in zip(artists, albums, songs)
    ]

@app.route('/', methods=['GET', 'POST'])
def home():
    return base('home', recommendations=recommendations())

@app.route('/songs', methods=['GET', 'POST'])
def songs():
    return base('songs', items=Song.query.all())

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    return base('albums', items=Album.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Wrong username or password.')
            return render_template('login.html', form=form)
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is not None:
            flash('Username already exists.')
            return render_template('signup.html', form=form)
        else:
            db.session.add(User(username=form.username.data, password=form.password.data))
            db.session.commit()
            return redirect(url_for('login'))
        
    return render_template('signup.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))