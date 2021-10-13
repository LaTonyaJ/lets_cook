from flask.globals import session
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Users, Favorites

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cook-test"

db.create_all()


class UserViewTest(TestCase):

    def setUp(self):
        self.client = app.test_client()

        db.drop_all()
        db.create_all()

        self.u = Users.register('username', 'password', 'Test', 'TestLast')
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_view(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.u.username

            resp = c.get(f"/favorites/{self.u.username}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', str(resp.data))

    def test_get_recipe(self):

        with self.client as c:

            meal = c.get('/recipe')
            self.assertIsNotNone(meal)
