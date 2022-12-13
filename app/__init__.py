from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
admin = Admin(app, template_mode='bootstrap4')
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

from .utils import create_logger
app.logger = create_logger()


from app import views, models
