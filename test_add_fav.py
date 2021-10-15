from app import app
from unittest import TestCase
from models import db

from models import Favorites, Users

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cook-test"

db.create_all()


class AddFavorite(TestCase):

    def setUp(self):

        self.client = app.test_client()

        Favorites.query.delete()
        Users.query.delete()

        self.user = Users.register('First', 'Last', 'Username', 'password')
        self.user.id = 3

        db.session.commit()

    def tearDown(self):

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_addFav(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = self.user.username

                fav = Favorites(users_id=self.user.id, img='image',
                                api_id='api', recipe_name='recipe')
                db.session.add(fav)
                db.session.commit()

                resp = c.get(f'/liked/{fav.api_id}')

                self.assertEqual(resp.status_code, 200)
                # self.assertIn('<h1>recipe</h1>', str(resp.data))
