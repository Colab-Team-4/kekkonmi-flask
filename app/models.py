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
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(32)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'email: {self.email} added to Users'




# Not sure if I have to wait for a template to make this part
class Venue(db.Model):
    id = db.Column(db.String, primary_key=True)
    price = db.Column(db.BigInteger, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, price, location, user_token):
        self.id = self.set_id()
        self.price = price
        self.location = location
        self.user_token = user_token
    
    def set_id(self):
        return str(uuid.uuid4())
        
    def __repr__(self):
        return f'Price: ${self.price} | Location: {self.location}'

class Event(db.Model):
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.BigInteger, nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, start_date, end_date, total_price, user_token):
        self.id = self.set_id()
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price
        self.user_token = user_token
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f'From {self.start_date} to {self.end_date} | Total Cost: ${self.total_price}'

