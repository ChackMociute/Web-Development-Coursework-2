from app import db
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import logout_user
from .models import User, Artist, Album, Song, FavoriteAlbum, FavoriteSong
from .forms import AlbumForm, SongForm, AlbumEditForm, SongEditForm
from sqlalchemy import func

from random import choice, choices, seed
from datetime import date
from time import mktime


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


def load_profile():
    user = User.query.get(int(session['_user_id']))
    album_form = AlbumForm()
    song_form = SongForm()
    if album_form.a_submit.data and album_form.validate_on_submit(): add_album(user, album_form)
    if song_form.s_submit.data and song_form.validate_on_submit(): add_song(user, song_form)
    if 'album_button' in request.form: remove_favorites(user, FavoriteAlbum, 'album')
    if 'song_button' in request.form: remove_favorites(user, FavoriteSong, 'song')
    return {'user': user, 'album_form': album_form, 'song_form': song_form}
    
def add_album(user, form):
    artist = get_artist(form.a_artist.data)
    album = get_item(Album, form.a_title.data, artist, year_released=form.year.data)
    association = FavoriteAlbum.query.filter(FavoriteAlbum.user == user, FavoriteAlbum.album == album).first()
    if association is None: user.favorite_albums.append(FavoriteAlbum(album=album, rating=form.a_score.data))
    elif form.a_score.data is not None: association.rating = form.a_score.data
    db.session.commit()
    flash("Album added successfully")

def add_song(user, form):
    artist = get_artist(form.s_artist.data)
    album = get_item(Album, form.album.data, artist) if form.album.data != '' else None
    song = get_item(Song, form.s_title.data, artist, album=album)
    association = FavoriteSong.query.filter(FavoriteSong.user == user, FavoriteSong.song == song).first()
    if association is None: user.favorite_songs.append(FavoriteSong(song=song, rating=form.s_score.data))
    elif form.s_score.data is not None: association.rating = form.s_score.data
    db.session.commit()
    flash("Song added successfully")

def get_artist(artist_name):
    artist = Artist.query.filter(func.lower(Artist.name) == artist_name.lower()).first()
    if artist is None:
        artist = Artist(name=artist_name)
        db.session.add(artist)
    return artist

def get_item(table, title, artist, **kwargs):
    item = table.query.filter(func.lower(table.title) == title.lower(), table.artist == artist).first()
    if item is None:
        item = table(title=title, artist=artist, **kwargs)
        db.session.add(item)
    for key, value in kwargs.items():
        if value is not None: setattr(item, key, value)
    return item

def remove_favorites(user, table, type):
    for id in request.form.getlist(f"{type}_id"):
        db.session.delete(table.query.get((user.id, int(id))))
    db.session.commit()


def edit_entry():
    album_update = session['last']['type'] == 'album'
    id = int(session['last']['id'])
    form = AlbumEditForm() if album_update else SongEditForm()
    item = Album.query.get(id) if album_update else Song.query.get(id)
    if form.validate_on_submit():
        if album_update: update_album_db(form, item)
        else: update_song_db(form, item)
        db.session.commit()
        return None
    return {'form': form, 'album': album_update, 'item':item}

def update_album_db(form, album):
    user = User.query.get(int(session['_user_id']))
    association = FavoriteAlbum.query.filter(FavoriteAlbum.user == user, FavoriteAlbum.album == album).first()
    if form.score.data is not None: association.rating = form.score.data
    if form.year.data is not None: album.year_released = form.year.data
    if form.songs.data != '': add_to_album(album, form.songs.data)

def update_song_db(form, song):
    user = User.query.get(int(session['_user_id']))
    association = FavoriteSong.query.filter(FavoriteSong.user == user, FavoriteSong.song == song).first()
    if form.score.data is not None: association.rating = form.score.data

def add_to_album(album, songs):
    for s in [s.strip() for s in songs.split(',') if s != '']:
        song = Song.query.filter(Song.title == s, Song.artist == album.artist).first()
        if song is None: song = Song(title=s, artist=album.artist)
        if song not in album.songs: album.songs.append(song)