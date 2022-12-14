from app import db, app
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import logout_user, login_user
from .models import User, Artist, Album, Song, FavoriteAlbum, FavoriteSong
from .forms import AlbumForm, SongForm, AlbumEditForm, SongEditForm
from sqlalchemy import func

from random import choice, sample, seed
from datetime import date
from time import mktime
import logging


# function for creating a logger with two levels of
# logging being saved in separate files
def create_logger():
    # Filter for only saving messages with an appropriate level of logging
    class LevelFilter(object):
        def __init__(self, level):
            self.level = level

        def filter(self, logRecord):
            return logRecord.levelno >= self.level
    
    logger = logging.getLogger('')
    
    # Handler for DEBUG level logs
    h1 = logging.FileHandler('logs/record.log')
    h1.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    h1.setLevel(logging.DEBUG)
    h1.addFilter(LevelFilter(logging.INFO))
    logger.addHandler(h1)

    # Handler for ERROR level logs
    h2 = logging.FileHandler('logs/errors.log')
    h2.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    h2.setLevel(logging.ERROR)
    h2.addFilter(LevelFilter(logging.ERROR))
    logger.addHandler(h2)
    logger.setLevel(logging.DEBUG)
    
    return logger

# Base function as a wrapper to render_template()
# used for providing ubiquitous needed support to most endpoints
def base(page, **kwargs):
    if '_user_id' in session:
        app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' opened {page} page.")
    else:
        app.logger.info(f"Guest user opened {page} page.")
    if 'login' in request.form:
        return redirect(url_for('login'))
    if 'signup' in request.form:
        return redirect(url_for('signup'))
    if 'password' in request.form:
        return redirect(url_for('change_password'))
    if 'logout' in request.form:
        app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' logged out.")
        logout_user()
        return redirect(url_for('home'))
    return render_template(f"{page}.html", **kwargs)

# Create 3 song daily recommendations used on home page
def recommendations():
    seed(mktime(date.today().timetuple()))
    artists = sample(Artist.query.join(Album).join(Song).all(), k=3)
    albums = [choice([album for album in artist.albums if len(album.songs) > 0]) for artist in artists]
    songs = [choice(album.songs) for album in albums]
    app.logger.info(f"Created daily recommendations")
    return [
        {'artist': artist, 'song': song, 'album': album}
        for artist, album, song
        in zip(artists, albums, songs)
    ]


# Function for loading and managing the profile page of users
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
    # Create or update the association between user and album
    if association is None: user.favorite_albums.append(FavoriteAlbum(album=album, rating=form.a_score.data))
    elif form.a_score.data is not None: association.rating = form.a_score.data
    db.session.commit()
    flash("Album added successfully")
    app.logger.info(f"User '{user.username}' succesfully added album with id {album.id}.")

def add_song(user, form):
    artist = get_artist(form.s_artist.data)
    album = get_item(Album, form.album.data, artist) if form.album.data != '' else None
    song = get_item(Song, form.s_title.data, artist, album=album)
    association = FavoriteSong.query.filter(FavoriteSong.user == user, FavoriteSong.song == song).first()
    # Create or update the association between user and song
    if association is None: user.favorite_songs.append(FavoriteSong(song=song, rating=form.s_score.data))
    elif form.s_score.data is not None: association.rating = form.s_score.data
    db.session.commit()
    flash("Song added successfully")
    app.logger.info(f"User '{user.username}' succesfully added album with id {song.id}.")

def get_artist(artist_name):
    artist = Artist.query.filter(func.lower(Artist.name) == artist_name.lower()).first()
    # If artist does not exist, create it
    if artist is None:
        artist = Artist(name=artist_name)
        db.session.add(artist)
    return artist

def get_item(table, title, artist, **kwargs):
    item = table.query.filter(func.lower(table.title) == title.lower(), table.artist == artist).first()
    # If item does not exist, create it
    if item is None:
        item = table(title=title, artist=artist, **kwargs)
        db.session.add(item)
    # Update the attributes of an item rather than create a new one if it already exists
    for key, value in kwargs.items():
        if value is not None: setattr(item, key, value)
    return item

def remove_favorites(user, table, type):
    # Find selected items
    ids = request.form.getlist(f"{type}_id")
    for id in ids:
        db.session.delete(table.query.get((user.id, int(id))))
    db.session.commit()
    # Only log when a deletion has been made
    if len(ids) > 0:
        app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' successfully removed {len(ids)} favorites.")


def try_login(form):
    user = User.query.filter(User.username == form.username.data).first()
    # If user does not exist in the database or the password does not match, login fails
    if user is None or not user.verify_password(form.password.data):
        flash('Wrong username or password.')
        app.logger.info("Guest user failed to log in.")
        return render_template('login.html', form=form)
    # If verification succeeds, login user
    login_user(user)
    app.logger.info(f"'{user.username}' logged in.")
    return redirect(url_for('home'))

def try_signup(form):
    user = User.query.filter(User.username == form.username.data).first()
    # If user with such a username already exists in a database, signup fails
    if user is not None:
        flash('Username already exists.')
        app.logger.info("User attempted to sign up with a taken username.")
        return render_template('signup.html', form=form)
    # If specified username does not exist, create user and redirect to login page
    db.session.add(User(username=form.username.data, password=form.password.data))
    db.session.commit()
    app.logger.info(f"User '{form.username.data}' created.")
    return redirect(url_for('login'))

def try_password_reset(form):
    user = User.query.get(int(session['_user_id']))
    # If user entered the correct password, change their password
    if user.verify_password(form.old.data):
        user.change_password(form.new.data)
        db.session.commit()
        app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' changed their password.")
        return redirect(url_for('profile'))
    # If the password was wrong, inform the user
    app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' failed to change their password.")
    flash("Incorrect password")
    return base('password', form=form)


# Function for altering and updating user favorites
def edit_entry():
    # Find what item needs updating
    album_update = session['last']['type'] == 'album'
    id = int(session['last']['id'])
    form = AlbumEditForm() if album_update else SongEditForm()
    item = Album.query.get(id) if album_update else Song.query.get(id)
    # If the user submits the form, update the entry
    if form.validate_on_submit():
        if album_update: update_album_db(form, item)
        else: update_song_db(form, item)
        db.session.commit()
        app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' "+
                        f"succesfully edited {session['last']['type']} with id {id}.")
        # Returning none because the update was successful
        # and there is no need to load the edit page anymore
        return None
    # Return arguments required for the update page
    return {'form': form, 'album': album_update, 'item':item}

def update_album_db(form, album):
    user = User.query.get(int(session['_user_id']))
    association = FavoriteAlbum.query.filter(FavoriteAlbum.user == user, FavoriteAlbum.album == album).first()
    # Update the columns entered by the user
    if form.score.data is not None: association.rating = form.score.data
    if form.year.data is not None: album.year_released = form.year.data
    if form.songs.data != '': add_to_album(album, form.songs.data)

def update_song_db(form, song):
    user = User.query.get(int(session['_user_id']))
    association = FavoriteSong.query.filter(FavoriteSong.user == user, FavoriteSong.song == song).first()
    # Update the columns entered by the user
    if form.score.data is not None: association.rating = form.score.data
    if form.album.data != '':
        album = Album.query.filter(func.lower(Album.title) == form.album.data.lower(), Album.artist == song.artist).first()
        if album is None: album = Album(title=form.album.data, artist=song.artist)
        song.album = album

def add_to_album(album, songs):
    # For every song the user has specified, add it to the album
    for s in [s.strip() for s in songs.split(',') if s != '']:
        song = Song.query.filter(Song.title == s, Song.artist == album.artist).first()
        # If the song does not exist, create it
        if song is None: song = Song(title=s, artist=album.artist)
        if song not in album.songs: album.songs.append(song)