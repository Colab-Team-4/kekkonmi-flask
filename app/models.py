from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import uuid, secrets

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String, default='', unique=True)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, password):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(32)

    def set_password(self, password):
        return generate_password_hash(password)

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'Email: {self.email} added to Users'

class Venue(db.Model):
    id = db.Column(db.String, primary_key=True)
    price = db.Column(db.Numeric(precision=12, scale=2))
    location = db.Column(db.String(150), nullable=False)
    tags = db.relationship('Tag', backref='venue', lazy=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, price, location, user_token, tags=None):
        self.id = str(uuid.uuid4())
        self.price = price
        self.location = location
        self.user_token = user_token
        if tags:
            self.tags = [Tag(tag_name=tag, venue_id=self.id) for tag in tags]

    def __repr__(self):
        return f'Price: ${self.price} | Location: {self.location}'

class Tag(db.Model):
    id = db.Column(db.String, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False)
    venue_id = db.Column(db.String, db.ForeignKey('venue.id'), nullable=False)

    def __init__(self, tag_name, venue_id):
        self.id = str(uuid.uuid4())
        self.tag_name = tag_name
        self.venue_id = venue_id

class Event(db.Model):
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(precision=10, scale=2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, start_date, end_date, total_price, user_token):
        self.id = str(uuid.uuid4())
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price
        self.user_token = user_token

    def __repr__(self):
        return f'From {self.start_date} to {self.end_date} | Total Cost: ${self.total_price}'

