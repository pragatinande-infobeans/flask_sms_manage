from flask import Flask
from smsmanagement import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # This connects BlogPosts to a User Author.
    # posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"UserName: {self.username}"


class Group(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    group_name = db.Column(db.String(100), nullable=False)
    group_description = db.Column(db.String(255), nullable=False)
    contacts = db.relationship('Contact', backref='group_ref', cascade='all, delete')

    def __init__(self, group_name, group_description, user_id):
        self.group_name = group_name
        self.group_description = group_description
        self.user_id = user_id

    def __repr__(self):
        return f"Group Id: {self.id} --- Date: {self.date} --- group_name: {self.group_name}"


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group', backref=db.backref('contacts_ref', lazy=True))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_nos = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)

    def __init__(self, contact_name, contact_nos, group_id, contact_email):
        self.contact_name = contact_name
        self.contact_nos = contact_nos
        self.contact_email = contact_email
        self.group_id = group_id

    def __repr__(self):
        return f"Contact User Id: {self.id} --- Date: {self.date} --- User Name: {self.contact_name}"