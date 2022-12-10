from app import app, db, admin, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, login_required
from .models import User, Artist, Album, Song, FavoriteAlbum, FavoriteSong
from .forms import LoginForm, AlbumForm, SongForm
from sqlalchemy import func

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
        return redirect(url_for('home'))
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

def add_album(user, form):
    artist = Artist.query.filter(func.lower(Artist.name) == form.a_artist.data.lower()).first()
    album = Album.query.filter(func.lower(Album.title) == form.a_title.data.lower(),
                               Album.artist == artist).first()
    if album is None:
        if artist is None:
            artist = Artist(name=form.a_artist.data)
            db.session.add(artist)
        album = Album(title=form.a_title.data, artist=artist, year_released=form.year.data)
        db.session.add(album)
    association = FavoriteAlbum.query.filter(FavoriteAlbum.user == user, FavoriteAlbum.album == album).first()
    if association is None:
        user.favorite_albums.append(FavoriteAlbum(album=album, rating=form.a_score.data))
    else:
        association.rating = form.a_score.data
    db.session.commit()

def add_song(user, form):
    artist = Artist.query.filter(func.lower(Artist.name) == form.s_artist.data.lower()).first()
    song = Song.query.filter(func.lower(Song.title) == form.s_title.data.lower(),
                            Album.artist == artist).first()
    if song is None:
        if artist is None:
            artist = Artist(name=form.s_artist.data)
            db.session.add(artist)
        if form.album.data is not None:
            album = Album.query.filter(func.lower(Album.title) == form.album.data.lower(),
                                       Album.artist == artist).first()
            if album is None:
                album = Album(title=form.album.data, artist=artist)
                db.session.add(album)
        song = Song(title=form.s_title.data, artist=artist, album=album)
        db.session.add(song)
    association = FavoriteSong.query.filter(FavoriteSong.user == user, FavoriteSong.song == song).first()
    if association is None:
        user.favorite_songs.append(FavoriteSong(song=song, rating=form.s_score.data))
    else:
        association.rating = form.s_score.data
    db.session.commit()

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(int(session['_user_id']))
    album_form = AlbumForm()
    song_form = SongForm()
    if album_form.a_submit.data and album_form.validate_on_submit():
        add_album(user, album_form)
        flash("Album added successfully")
    if song_form.s_submit.data and song_form.validate_on_submit():
        add_song(user, song_form)
    return base('profile', user=user, album_form=album_form, song_form=song_form)

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
    return base('login', form=form)

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
        
    return base('signup', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))