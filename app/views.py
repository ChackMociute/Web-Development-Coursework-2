from app import app, db, admin, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, login_required
from .models import User, Artist, Album, Song
from .forms import LoginForm, PasswordChangeForm
from .utils import base, recommendations, load_profile, edit_entry

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
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Wrong username or password.')
            app.logger.info("Guest user failed to log in.")
            return render_template('login.html', form=form)
        else:
            login_user(user)
            app.logger.info(f"'{user.username}' logged in.")
            return redirect(url_for('home'))
    return base('login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is not None:
            flash('Username already exists.')
            app.logger.info("User attempted to sign up with a taken username.")
            return render_template('signup.html', form=form)
        else:
            db.session.add(User(username=form.username.data, password=form.password.data))
            db.session.commit()
            app.logger.info(f"User '{form.username.data}' created.")
            return redirect(url_for('login'))
    return base('signup', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return base('profile', **load_profile())

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def update():
    update = edit_entry()
    if update is None: return redirect(url_for('profile'))
    return base('edit', **update)

@app.route('/profile/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        user = User.query.get(int(session['_user_id']))
        if user.verify_password(form.old.data):
            user.change_password(form.new.data)
            db.session.commit()
            app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' changed their password.")
            return redirect(url_for('profile'))
        else:
            app.logger.info(f"User '{User.query.get(int(session['_user_id'])).username}' failed to change their password.")
            flash("Incorrect password")
    return base('password', form=form)

@app.route('/edit', methods=['POST'])
def edit():
    data = json.loads(request.data)
    type, id = *data.get('id').split(','),
    session['last'] = {'type': type, 'id': id}
    
    return json.dumps({'status': 'OK', 'id': id, 'type': type})

@app.route('/select', methods=['POST'])
def select():
    data = json.loads(request.data)
    type, artist_id, id = *data.get('id').split(','),
    artist = Artist.query.get(int(artist_id))
    data = artist.songs if type == 'songs' else artist.albums
    data = [{'title': d.title, 'score': d.mean_score()} for d in
            sorted(data, key=lambda x: 0 if x.mean_score() is None else x.mean_score(), reverse=True)]
    try: prev, session['prev'] = session['prev'], id
    except KeyError: prev = session['prev'] = id

    return json.dumps({'status': 'OK', 'data': data, 'artist': artist.name, 'type': type.title(), 'id': id, 'prev': prev})

@app.route('/albumSongs', methods=['POST'])
def album_songs():
    id = int(json.loads(request.data).get('id'))
    album = Album.query.get(id)
    data = [{'title': s.title, 'score': s.mean_score()} for s in
            sorted(album.songs, key=lambda x: 0 if x.mean_score() is None else x.mean_score(), reverse=True)]
    try: prev, session['prev'] = session['prev'], id
    except KeyError: prev = session['prev'] = id

    return json.dumps({'status': 'OK', 'data': data, 'album': album.title, 'id': id, 'prev': prev})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))