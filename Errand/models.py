from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    profile_picture = db.Column(db.String(255))
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('requests', lazy=True))

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='open')
    last_updated = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    closed_at = db.Column(db.DateTime)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), unique=True)
    responder_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request = db.relationship('Request', backref=db.backref('chat', uselist=False), lazy=True)
    responder = db.relationship('User', foreign_keys=[responder_id], backref='chats_responded', lazy=True)
    requester = db.relationship('User', foreign_keys=[requester_id], backref='chats_requested', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    multimedia_url = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat = db.relationship('Chat', backref=db.backref('messages', lazy=True))
    sender = db.relationship('User', backref='messages_sent', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
# There is possibility for somechanges to be made here 