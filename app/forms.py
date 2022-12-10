from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('password', validators=[DataRequired()])

class AlbumForm(FlaskForm):
    a_title = StringField('title', validators=[DataRequired(), Length(max=200)], render_kw={'placeholder': 'Title'})
    a_artist = StringField('artist', validators=[DataRequired(), Length(max=150)], render_kw={'placeholder': 'Artist'})
    year = IntegerField('year', validators=[Optional(), NumberRange(min=0, max=date.today().year + 1)], render_kw={'placeholder': 'Year (optional)'})
    a_submit = SubmitField('Add')

class SongForm(FlaskForm):
    s_title = StringField('title', validators=[DataRequired(), Length(max=200)], render_kw={'placeholder': 'Title'})
    s_artist = StringField('artist', validators=[DataRequired(), Length(max=150)], render_kw={'placeholder': 'Artist'})
    album = StringField('album', validators=[Optional(), Length(max=200)], render_kw={'placeholder': 'Album (optional)'})
    s_submit = SubmitField('Add')