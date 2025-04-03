from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Ассоциативная таблица для участников игры
participants = db.Table('participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    
    # Игры, которые пользователь создал
    created_games = db.relationship('Game', backref='organizer', lazy=True)
    
    # Игры, в которых пользователь участвует
    games = db.relationship('Game', secondary=participants, backref=db.backref('participants', lazy='dynamic'))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    min_player_count = db.Column(db.Integer, nullable=False)
    max_player_count = db.Column(db.Integer, nullable=False)
    player_count = db.Column(db.Integer, nullable=False)

    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_time = db.Column(db.DateTime, nullable=False)
    
    # Организатор игры
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)