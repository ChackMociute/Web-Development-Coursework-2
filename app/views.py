from app import app, db, admin
from flask import render_template
from flask_admin.contrib.sqla import ModelView
from .models import User, Artist, Album, Song

from random import choice, choices, seed
from datetime import date
from time import mktime

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Artist, db.session))
admin.add_view(ModelView(Album, db.session))
admin.add_view(ModelView(Song, db.session))


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

@app.route('/')
def home():
    return render_template('home.html', recommendations=recommendations())