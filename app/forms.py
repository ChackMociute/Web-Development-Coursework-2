from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import date

# Form for logging in as well as signing up
class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired()])

class PasswordChangeForm(FlaskForm):
    old = PasswordField('old_password', validators=[DataRequired()])
    new = PasswordField('new_password', validators=[DataRequired()])

# Form for adding a new album into the database
class AlbumForm(FlaskForm):
    a_title = StringField('title', validators=[DataRequired(), Length(max=200)], render_kw={'placeholder': 'Title'})
    a_artist = StringField('artist', validators=[DataRequired(), Length(max=150)], render_kw={'placeholder': 'Artist'})
    year = IntegerField('year', validators=[Optional(), NumberRange(min=0, max=date.today().year + 1)], render_kw={'placeholder': 'Release year (optional)'})
    a_score = FloatField('rating', validators=[Optional(), NumberRange(min=0, max=100)], render_kw={'placeholder': 'Score (optional)'})
    a_submit = SubmitField('Add')

# Form for adding a new song into the database
class SongForm(FlaskForm):
    s_title = StringField('title', validators=[DataRequired(), Length(max=200)], render_kw={'placeholder': 'Title'})
    s_artist = StringField('artist', validators=[DataRequired(), Length(max=150)], render_kw={'placeholder': 'Artist'})
    album = StringField('album', validators=[Optional(), Length(max=200)], render_kw={'placeholder': 'Album (optional)'})
    s_score = FloatField('rating', validators=[Optional(), NumberRange(min=0, max=100)], render_kw={'placeholder': 'Score (optional)'})
    s_submit = SubmitField('Add')

class EditForm(FlaskForm):
    score = FloatField('rating', validators=[Optional(), NumberRange(min=0, max=100)])
    submit = SubmitField('Add')

# Form for updating and amending albums
class AlbumEditForm(EditForm):
    year = IntegerField('year', validators=[Optional(), NumberRange(min=0, max=date.today().year + 1)])
    songs = TextAreaField('songs', validators=[Optional()])

# Form for updating and amending songs
class SongEditForm(EditForm):
    album = StringField('title', validators=[Optional(), Length(max=200)])