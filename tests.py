from app import app, db
from sqlalchemy import func
from app.models import User, Artist, Album, Song, FavoriteAlbum, FavoriteSong

import os
import unittest


class DatabaseTestSuite(unittest.TestCase):
    def populate_db(self):
        self.user = User(username='user1', password='pass1')
        self.artist = Artist(name='artist1')
        self.album = Album(title='album1', artist=self.artist, year_released=2000)
        self.song = Song(title='song1', artist=self.artist, album=self.album)
        db.session.add(self.user)
        db.session.add(self.artist)
        db.session.add(self.album)
        db.session.add(self.song)
        
        ar = Artist(name='artist2')
        al = Album(title='album2', artist=ar)
        db.session.add(ar)
        db.session.add(al)
        
        ar = Artist(name='artist3')
        s = Song(title='song2', artist=ar)
        db.session.add(ar)
        db.session.add(s)
        
        ar = Artist(name='artist4')
        al = Album(title='album3', artist=ar)
        s = Song(title='song.', artist=ar, album=al)
        db.session.add(ar)
        db.session.add(al)
        db.session.add(s)
        self.artists_with_albums_with_songs = [self.artist, ar]
        
        u = User(username='user2', password='pass2')
        db.session.add(u)
        
        a = FavoriteSong(user=self.user, song=self.song, rating=75)
        db.session.add(a)
        a = FavoriteAlbum(user=self.user, album=self.album, rating=75)
        db.session.add(a)
        a = FavoriteSong(user=self.user, song=s, rating=75)
        db.session.add(a)
        a = FavoriteAlbum(user=self.user, album=al, rating=75)
        db.session.add(a)
        a = FavoriteSong(user=u, song=self.song, rating=85)
        db.session.add(a)
        a = FavoriteAlbum(user=u, album=self.album, rating=85)
        db.session.add(a)
        
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        # app.config['SECRET_KEY'] = 'TEST KEY'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        
        self.app = app.test_client()
        db.create_all()
        self.populate_db()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_query_user_id(self):
        self.assertEqual(User.query.get(1), self.user)
        self.assertEqual(Artist.query.get(1), self.artist)
        self.assertEqual(Album.query.get(1), self.album)
        self.assertEqual(Song.query.get(1), self.song)
        
    def test_query_by_attributes(self):
        artist = Artist.query.filter_by(name='artist1').first()
        self.assertEqual(User.query.filter_by(username='user1').first(), self.user)
        self.assertEqual(Artist.query.filter_by(name='artist1').first(), self.artist)
        self.assertEqual(Album.query.filter_by(title='album1', artist=artist).first(), self.album)
        self.assertEqual(Song.query.filter_by(title='song1', artist=artist).first(), self.song)
        
    def test_query_by_attributes_ignore_case(self):
        artist = Artist.query.filter_by(name='artist1').first()
        self.assertEqual(User.query.filter(func.lower(User.username) == 'uSeR1'.lower()).first(), self.user)
        self.assertEqual(Artist.query.filter(func.lower(Artist.name) == 'ARtIsT1'.lower()).first(), self.artist)
        self.assertEqual(Album.query.filter(func.lower(Album.title) == 'albUM1'.lower(), Album.artist == artist).first(), self.album)
        self.assertEqual(Song.query.filter(func.lower(Song.title) == 'SONg1'.lower(), Song.artist == artist).first(), self.song)
    
    def test_query_for_artists_with_albums_with_songs(self):
        self.assertEqual(Artist.query.join(Album).join(Song).all(), self.artists_with_albums_with_songs)
        
    def test_query_for_nonexistant(self):
        self.assertIsNone(User.query.get(-1))
        self.assertIsNone(Artist.query.get(-1))
        self.assertIsNone(Album.query.get(-1))
        self.assertIsNone(Song.query.get(-1))
        
    def test_many_to_many(self):
        self.assertEqual(User.query.get(1).favorite_songs, self.user.favorite_songs)
        self.assertEqual(User.query.get(1).favorite_albums, self.user.favorite_albums)
    
    def test_mean_rating(self):
        self.assertEqual(Album.query.get(1).mean_score(), 80)
        self.assertEqual(Song.query.get(1).mean_score(), 80)
        
    def test_password_verification(self):
        self.assertTrue(self.user.verify_password('pass1'))
        self.assertFalse(self.user.verify_password('pass2'))
        
    def test_password_change(self):
        self.user.change_password('pass2')
        db.session.add(self.user)
        self.assertFalse(self.user.verify_password('pass1'))
        self.assertTrue(self.user.verify_password('pass2'))
    
    def test_existing_attributes(self):
        self.assertEqual(User.query.get(1).username, self.user.username)
        self.assertEqual(User.query.get(1).password, self.user.password)
        self.assertEqual(User.query.get(1).favorite_songs, self.user.favorite_songs)
        self.assertEqual(User.query.get(1).favorite_albums, self.user.favorite_albums)
        
        self.assertEqual(Artist.query.get(1).name, self.artist.name)
        self.assertEqual(Artist.query.get(1).albums, self.artist.albums)
        self.assertEqual(Artist.query.get(1).songs, self.artist.songs)
        
        self.assertEqual(Album.query.get(1).title, self.album.title)
        self.assertEqual(Album.query.get(1).year_released, self.album.year_released)
        self.assertEqual(Album.query.get(1).artist, self.album.artist)
        self.assertEqual(Album.query.get(1).songs, self.album.songs)
        
        self.assertEqual(Song.query.get(1).title, self.song.title)
        self.assertEqual(Song.query.get(1).artist, self.song.artist)
        self.assertEqual(Song.query.get(1).album, self.song.album)
    
    def test_nonexistant_attributes(self):
        self.assertFalse(Artist.query.get(2).songs)
        self.assertFalse(Artist.query.get(3).albums)
        
        self.assertIsNone(Album.query.get(2).year_released)
        self.assertFalse(Album.query.get(2).songs)
        
        self.assertIsNone(Song.query.get(2).album)


if __name__ == '__main__':
    unittest.main()