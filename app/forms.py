from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired()])

class AlbumForm(FlaskForm):
    a_title = StringField('title', validators=[DataRequired(), Length(max=200)], render_kw={'placeholder': 'Title'})
    a_artist = StringField('artist', validators=[DataRequired(), Length(max=150)], render_kw={'placeholder': 'Artist'})
    year = IntegerField('year', validators=[Optional(), NumberRange(min=0, max=date.today().year + 1)], render_kw={'placeholder': 'Release year (optional)'})
    a_score = FloatField('rating', validators=[Optional(), NumberRange(min=0, max=100)], render_kw={'placeholder': 'Score (optional)'})
    a_submit = SubmitField('Add')

class SongForm(FlaskForm):
    s_title = StringField('title', validators=[DataRequired(), Length(max=200)], render_kw={'placeholder': 'Title'})
    s_artist = StringField('artist', validators=[DataRequired(), Length(max=150)], render_kw={'placeholder': 'Artist'})
    album = StringField('album', validators=[Optional(), Length(max=200)], render_kw={'placeholder': 'Album (optional)'})
    s_score = FloatField('rating', validators=[Optional(), NumberRange(min=0, max=100)], render_kw={'placeholder': 'Score (optional)'})
    s_submit = SubmitField('Add')

class EditForm(FlaskForm):
    score = FloatField('rating', validators=[Optional(), NumberRange(min=0, max=100)])
    submit = SubmitField('Add')

class AlbumEditForm(EditForm):
    year = IntegerField('year', validators=[Optional(), NumberRange(min=0, max=date.today().year + 1)])
    songs = TextAreaField('songs', validators=[Optional()])

class SongEditForm(EditForm):
    album = StringField('title', validators=[Optional(), Length(max=200)])