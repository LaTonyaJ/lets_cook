from app import app
from models import Favorites, Instructions, Users, db
from unittest import TestCase

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cook-test"

db.create_all()


class TestFavorites(TestCase):

    def setUp(self):
        self.client = app.test_client()
        Favorites.query.delete()
        Users.query.delete()

        self.u = Users.register('First', 'Last', 'Username', 'password')
        self.u.id = 99
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        return super().tearDown()

    def test_fav_model(self):

        fav = Favorites(users_id=self.u.id, img='image',
                        api_id='api_id', recipe_name='Recipe')
        db.session.add(fav)
        db.session.commit()

        self.assertIsNotNone(fav)
        self.assertEqual(self.u.id, fav.users_id)

    def test_instruction_model(self):

        fav = Favorites(users_id=99, img='image',
                        api_id='id', recipe_name='Name')

        db.session.add(fav)
        db.session.commit()

        i = Instructions(favorites_id=fav.id,
                         steps='StepsStepsSteps StepsStepsSteps')

        db.session.add(i)
        db.session.commit()

        self.assertIsNotNone(i)
        self.assertEqual(i.get_steps, ['StepsStepsSteps StepsStepsSteps'])
