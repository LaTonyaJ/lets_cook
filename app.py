from flask import Flask, request
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from models import db, connect_db, Users, Favorites, Meals
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///lets_cook"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

app.config['SECRET_KEY'] = 'Whatz4DiNNer?2nite'
debug = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    return render_template('base.html')


@app.route('/todays_recipe')
def random_recipe():
    rr = requests.get('http://www.themealdb.com/api/json/v1/1/random.php')
    resp = rr.json()
    meal = Meals(title=resp['meals'][0]['strMeal'],
                 img=resp['meals'][0]['strMealThumb'],
                 instructions=resp['meals'][0]['strInstructions'])
    print(resp['meals'][0])
    # print(rr.status_code)
    db.session.add(meal)
    db.session.commit()

    return render_template('random.html', resp=resp)


@app.route('/favorites/<users_id>')
def user_fav_recipes(users_id):

    # favs = Favorites(users_id=users_id, meal_id=)
    return render_template('favorites.html')
