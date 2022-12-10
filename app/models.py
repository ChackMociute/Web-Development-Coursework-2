from app import db, bcrypt
from flask_login import UserMixin


class FavoriteSong(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    user = db.relationship('User', back_populates='favorite_songs')
    song = db.relationship('Song', back_populates='favored')
    rating = db.Column(db.Float)

class FavoriteAlbum(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), primary_key=True)
    user = db.relationship('User', back_populates='favorite_albums')
    album = db.relationship('Album', back_populates='favored')
    rating = db.Column(db.Float)

class User(db.Model, UserMixin):
    def __init__(self, password=None, **kwargs):
        if password is not None: kwargs['password'] = self.encrypt_password(password)
        super(User, self).__init__(**kwargs)
        
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    password = db.Column(db.BINARY)
    favorite_songs = db.relationship('FavoriteSong', back_populates='user')
    favorite_albums = db.relationship('FavoriteAlbum', back_populates='user')
    
    def encrypt_password(self, password):
        return bcrypt.generate_password_hash(password)
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def __repr__(self):
        return self.username

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    albums = db.relationship('Album', back_populates='artist')
    songs = db.relationship('Song', back_populates='artist')
    
    def __repr__(self):
        return self.name

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    year_released = db.Column(db.Integer, index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', back_populates='albums')
    songs = db.relationship('Song', back_populates='album')
    favored = db.relationship('FavoriteAlbum', back_populates='album')
    
    def __repr__(self):
        return self.title

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', back_populates='songs')
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', back_populates='songs')
    favored = db.relationship('FavoriteSong', back_populates='song')
    
    def __repr__(self):
        return self.title