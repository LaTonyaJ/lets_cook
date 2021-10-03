from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db = SQLAlchemy()

bcrypt = Bcrypt()


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

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode('utf8')

        user = cls(username=username, password=hashed_utf8,
                   first_name=first_name, last_name=last_name)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Is your password right?"""

        user = Users.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    favs = db.relationship('Favorites', backref='user')


class Meals(db.Model):

    __tablename__ = 'meals'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    api_id = db.Column(db.Text, unique=True)


class Favorites(db.Model):

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, unique=True, primary_key=True)

    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    meals_id = db.Column(db.Integer, db.ForeignKey('meals.id'))

    img = db.Column(db.Text)
