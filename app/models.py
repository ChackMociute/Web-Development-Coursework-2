from app import db

favorite_song = db.Table('favorite_song', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

favorite_album = db.Table('favorite_album', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True)
    favorite_songs = db.relationship('Song', secondary=favorite_song)
    favorite_albums = db.relationship('Album', secondary=favorite_album)
    
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
    
    def __repr__(self):
        return self.title

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship('Artist', back_populates='songs')
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', back_populates='songs')
    
    def __repr__(self):
        return self.title