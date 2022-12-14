from app import app, db, admin, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from .models import User, Artist, Album, Song
from .forms import LoginForm, PasswordChangeForm
from .utils import base, recommendations, load_profile, edit_entry, try_login, try_signup, try_password_reset

import json

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Artist, db.session))
admin.add_view(ModelView(Album, db.session))
admin.add_view(ModelView(Song, db.session))


@app.route('/', methods=['GET', 'POST'])
def home():
    return base('home', recommendations=recommendations())

@app.route('/songs', methods=['GET', 'POST'])
def songs():
    return base('songs', items=sorted(Song.query.all(),
                                       key=lambda x: 0 if x.mean_score() is None
                                       else x.mean_score(), reverse=True))

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    return base('albums', items=sorted(Album.query.all(),
                                       key=lambda x: 0 if x.mean_score() is None
                                       else x.mean_score(), reverse=True))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): return try_login(form)
    return base('login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit(): return try_signup(form)
    return base('signup', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return base('profile', **load_profile())

@app.route('/profile/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit(): return try_password_reset(form)
    return base('password', form=form)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
# Endpoint for making adjustments to album and song entries
def update():
    update = edit_entry()
    # If None is returned by edit_entry(), the update was
    # successful and user is returned to profile page
    if update is None: return redirect(url_for('profile'))
    # Otherwise load the edit page with required arguments
    return base('edit', **update)

@app.route('/edit', methods=['POST'])
# Endpoint for ajax to determine where to place and remove gear icon
def edit():
    data = json.loads(request.data)
    type, id = *data.get('id').split(','),
    # Remember what item was selected for editing
    session['last'] = {'type': type, 'id': id}
    
    return json.dumps({'status': 'OK', 'id': id, 'type': type})

@app.route('/select', methods=['POST'])
# Endpoint for ajax to display all the specified items belonging to an artist
def select():
    data = json.loads(request.data)
    type, artist_id, id = *data.get('id').split(','),
    artist = Artist.query.get(int(artist_id))
    # Get an artist's song or album titles and ratings based on the user request
    data = artist.songs if type == 'songs' else artist.albums
    data = [{'title': d.title, 'score': d.mean_score()} for d in
            sorted(data, key=lambda x: 0 if x.mean_score() is None else x.mean_score(), reverse=True)]
    # Record in the session which item was requested last
    try: prev, session['prev'] = session['prev'], id
    except KeyError: prev = session['prev'] = id

    return json.dumps({'status': 'OK', 'data': data, 'artist': artist.name, 'type': type.title(), 'id': id, 'prev': prev})

@app.route('/albumSongs', methods=['POST'])
# Endpoint for ajax to display every song of an album
def album_songs():
    id = int(json.loads(request.data).get('id'))
    album = Album.query.get(id)
    # Get the songs and their ratings
    data = [{'title': s.title, 'score': s.mean_score()} for s in
            sorted(album.songs, key=lambda x: 0 if x.mean_score() is None else x.mean_score(), reverse=True)]
    # Record in the session which item was requested last
    try: prev, session['prev'] = session['prev'], id
    except KeyError: prev = session['prev'] = id

    return json.dumps({'status': 'OK', 'data': data, 'album': album.title, 'id': id, 'prev': prev})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))