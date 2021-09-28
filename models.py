from enum import unique
from operator import itemgetter
from os import name
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    username = db.Column(db.String(20), unique=True, nullable=False)

    password = db.Column(db.Text, nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name}{self.last_name}'

    @classmethod
    def register(cls, username, password, first_name, last_name):

        user = cls(username=username, password=password,
                   first_name=first_name, last_name=last_name)

        db.session.add(user)
        return user


class Meals(db.Model):

    __tablename__ = 'meals'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(30))
    img = db.Column(db.Text)
    instructions = db.Column(db.Text)


class Favorites(db.Model):

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    meals_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
