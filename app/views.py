from app import app, db, admin
from flask import render_template
from flask_admin.contrib.sqla import ModelView
from .models import User, Artist, Album, Song

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Artist, db.session))
admin.add_view(ModelView(Album, db.session))
admin.add_view(ModelView(Song, db.session))


@app.route('/')
def home():
    return render_template('music.html')