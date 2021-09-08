from flask_sqlalchemy import SQLAlchemy
import uuid
import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key= True, unique = True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True, nullable = False, default = '')
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    player = db.relationship('Player', backref = 'owner', lazy = True)

    def __init__(self, email, password, token = '', id =''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.get_token(12)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def get_token(self, length):
        return secrets.token_hex(length)

class Player(db.Model):
    id = db.Column(db.String, primary_key= True, unique = True)
    name = db.Column(db.String(150), nullable = False)
    team = db.Column(db.String, nullable = False)
    position = db.Column(db.String, nullable = False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'))

    def __init__(self, name, team, position, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.team = team
        self.position = position
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
        

class PlayerSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'team', 'position']

# Create a singular Data point return
player_schema = PlayerSchema()

# Create multiple data point return
players_schema = PlayerSchema(many = True)

