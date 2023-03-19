from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Define app.
app = Flask(__name__)               

# Config object.
app.config.from_object(Config)      

# Database instance.
db = SQLAlchemy(app)

# Database migration engine.
migrate = Migrate(app, db)          

# Flask login extension. Set up quiet notifications.
login = LoginManager(app)
login.login_message = None

# Tell login which route to redirect to for logins.
login.login_view = 'login'

from app import routes, models