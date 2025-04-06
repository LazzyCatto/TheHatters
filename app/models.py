from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Ассоциативная таблица для участников игры
participants = db.Table('participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

# Ассоциативная таблица для зарегистрированных на игры
pending_participants = db.Table('pending_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    about = db.Column(db.String(500))
    avatar = db.Column(db.String(120), default='default_avatar.png')

    password_hash = db.Column(db.String(128), nullable=False)
    
    # Игры, которые пользователь создал
    created_games = db.relationship('Game', backref='organizer', lazy=True)
    
    # Игры, в которых пользователь участвует
    joined_games = db.relationship('Game', secondary=participants, backref=db.backref('participants', lazy='dynamic'))

    # Игры, в которые пользователь только зарегистрировался
    pending_games = db.relationship('Game', secondary=participants, backref=db.backref('pending_participants', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_avatar(self):
        return f'avatars/{self.avatar}'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(500), nullable=True)

    min_player_count = db.Column(db.Integer, nullable=False)
    max_player_count = db.Column(db.Integer, nullable=False)
    player_count = db.Column(db.Integer, nullable=False)

    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_time = db.Column(db.DateTime, nullable=False)

    validation = db.Column(db.Boolean, nullable=False)
    
    # Организатор игры
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
