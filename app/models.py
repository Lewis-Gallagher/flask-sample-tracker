from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User(UserMixin, db.Model):
    id: int
    username: str
    email: str
    password_hash: str

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

@dataclass
class Project(db.Model):
    id: int
    name: str
    timestamp: datetime
    author: User.id

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, index = True, unique = True)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow())
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    
@dataclass
class Sample(db.Model):
    id: int
    name: str
    project: Project.id
    timestamp: datetime
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, index = True, unique = True)
    project = db.Column(db.Integer, db.ForeignKey('project.id'))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow())

@login.user_loader
def load_user(id):
    return User.query.get(int(id))