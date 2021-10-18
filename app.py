from flask import Flask, request, session, g
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from models import Ingredients, db, connect_db, Users, Favorites, Instructions
import requests
from forms import SignUp, Login, Filter
import pdb
from sqlalchemy.exc import IntegrityError
import random
import re
import os
from config import SECRET_KEY
import psycopg2

app = Flask(__name__)

# uri = 'postgresql+psycopg2://usernmae:password@host:port/dbname'
# if uri and uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
ENV = 'prod'

if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///lets_cook"
else:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    app.config['SQLALCHEMY_DATABASE_URI'] = conn

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
debug = DebugToolbarExtension(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add user to Flask global."""

    if 'username' in session:
        g.user = Users.query.filter(
            Users.username == session['username']).first()

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session['username'] = user.username.lower()


def do_logout():
    """Logout user."""

    if 'username' in session:
        del session['username']


@app.route('/')
def homepage():
    """Redirect to Random Recipe"""
    return redirect('/recipe')


@app.route('/recipe', methods=['GET', 'POST'])
def random_recipe():

    try:
        rr = requests.get('http://www.themealdb.com/api/json/v1/1/random.php')
        resp = rr.json()

        api_id = resp['meals'][0]['idMeal']
        steps = re.split(r'STEP|[\n\r]',
                         resp['meals'][0]['strInstructions'])

        form = Filter()

        if form.validate_on_submit():
            try:
                category = form.category.data
                rr = requests.get(
                    f'http://www.themealdb.com/api/json/v1/1/filter.php?c={category}')
                resp0 = rr.json()
                i = random.randrange(10)
                api_id = resp0['meals'][i]['idMeal']
                resp = requests.get(
                    f'http://www.themealdb.com/api/json/v1/1/lookup.php?i={api_id}')
                resp_json = resp.json()
                steps = re.split(r'STEP|[\r\n]',
                                 resp_json['meals'][0]['strInstructions'])
                return render_template('random.html', i=0, resp=resp_json, api_id=api_id, form=form, steps=steps)

            except TypeError:
                return redirect('/')

        else:
            i = 0
            return render_template('random.html', i=i, resp=resp, api_id=api_id, form=form, steps=steps)

    except IntegrityError:
        return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    """Register a new user"""

    if 'username' in session:
        # flash(session['username'])
        return redirect(f"/favorites/{session['username']}")

    form = SignUp()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data.lower()
        password = form.password.data

        new_user = Users.register(
            username, password, first_name, last_name)

        db.session.commit()
        do_login(new_user)
        flash('User added!')
        return redirect('/')

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login_form():
    """User login"""

    if 'username' in session:
        return redirect(f"/favorites/{session['username']}")

    form = Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        new_user = Users.authenticate(username, password)

        if new_user:
            do_login(new_user)
            return redirect(f"/favorites/{session['username']}")
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('signup.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log out user"""
    do_logout()
    # session.pop('username')
    return redirect('/login')


@app.route('/favorites/<username>')
def user_fav_recipes(username):

    if "username" not in session:

        flash('Must Login to like')
        return redirect('/')

    # session_username = session['username']
    # pdb.set_trace()
    user = Users.query.filter_by(username=session['username']).first()
    return render_template('favorites.html', user=user)


@app.route('/liked/<int:api_id>')
def liked(api_id):

    if 'username' not in session:
        flash('Must Login to Like!')
        return redirect('/')
    try:

        # add meal to fav
        meal = requests.get(
            f"http://www.themealdb.com/api/json/v1/1/lookup.php?i={api_id}")
        # pdb.set_trace()
        user = Users.query.filter_by(username=session['username']).first()
        # get meal by id

        resp = meal.json()
        fav = Favorites(
            users_id=user.id, img=resp['meals'][0]['strMealThumb'], api_id=resp['meals'][0]['idMeal'], recipe_name=resp['meals'][0]['strMeal'])

        db.session.add(fav)
        db.session.commit()

        steps = Instructions(favorites_id=fav.id,
                             steps=resp['meals'][0]['strInstructions'])

        items = []
        for i in range(1, 20):
            if resp['meals'][0][f'strIngredient{i}'] != None:
                items.append(resp['meals'][0][f'strIngredient{i}'])
                i = i + 1

        ings = Ingredients(favorites_id=fav.id, items=items)

        db.session.add(steps)
        db.session.add(ings)
        db.session.commit()
        return redirect(f"/favorites/{session['username']}")

    except IntegrityError:
        print()
        flash('Favorite not Added!')
        return redirect('/')


@app.route('/favorite/<int:favorites_id>')
def show_fav(favorites_id):

    fav = Favorites.query.get(favorites_id)
    instructions = Instructions.query.get(favorites_id)
    items = Ingredients.query.get(favorites_id)

    return render_template('favorite.html', fav=fav, instructions=instructions, items=items)


@app.route('/delete/<int:favorites_id>', methods=['POST'])
def remove_favorite(favorites_id):

    fav = Favorites.query.get(favorites_id)
    db.session.delete(fav)
    db.session.commit()

    return redirect(url_for('user_fav_recipes', username=session['username']))
