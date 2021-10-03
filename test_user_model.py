from flask.globals import session
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Users

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cook-test"

db.create_all()


class UserModelTest(TestCase):

    def setUp(self):
        Users.query.delete()
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):

        u = Users(first_name='test', last_name='testLast',
                  username='user', password='password')

        db.session.add(u)
        db.session.commit()

        self.assertIsNotNone(u)

    def test_user_register(self):

        u = Users.register(first_name='test', last_name='testLast',
                           username='username', password='password')

        db.session.add(u)

        self.assertEqual(u.username, 'username')
        self.assertNotEqual(u.password, 'password')
        self.assertTrue(u.password.startswith('$2b$'))

    def test_user_authenticate(self):

        user = Users.register('username', 'password', 'test', 'testLast')
        db.session.add(user)

        u = Users.authenticate(user.username, 'password')

        self.assertEqual(user.id, u.id)

    def test_invalid_input(self):

        user = Users.register(None, 'password', 'Test', 'TestLast')
        user.id = 889
        db.session.add(user)

        self.assertRaises(exc.IntegrityError)
