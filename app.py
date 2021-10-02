from flask import Flask, request, session
from flask.helpers import flash
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import redirect
from models import db, connect_db, Users, Favorites, Meals
import requests
from forms import SignUp, Login
import pdb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///lets_cook"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = 'Whatz4DiNNer?2nite'
debug = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    """Redirect to Random Recipe"""
    return redirect('/recipe')


@app.route('/recipe')
def random_recipe():

    rr = requests.get('http://www.themealdb.com/api/json/v1/1/random.php')
    resp = rr.json()
    meal = Meals(api_id=resp['meals'][0]['idMeal'])
    print(resp['meals'][0])
    # print(rr.status_code)
    db.session.add(meal)
    db.session.commit()

    return render_template('random.html', resp=resp, meal=meal)


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
        session['username'] = new_user.username
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
            session['username'] = new_user.username.lower()
            return redirect(f"/favorites/{session['username']}")
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('signup.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log out user"""

    session.pop('username')
    return redirect('/login')


@app.route('/favorites/<username>')
def user_fav_recipes(username):

    if "username" not in session:

        flash('Must Login to like')
        return redirect('/')

    session_username = session['username']
    user = Users.query.filter(username == session_username).first()
    return render_template('favorites.html', user=user)


@app.route('/liked/<int:meals_id>')
def liked(meals_id):

    if 'username' not in session:
        return redirect('/')

    # add meal to fav
    meal = Meals.query.get(meals_id)
    username = session['username']
    # pdb.set_trace()
    user = Users.query.filter(Users.username == username).first()
    fav = Favorites(users_id=user.id, meals_id=meal.id)

    db.session.add(fav)
    db.session.commit()
    return redirect(f"/favorites/{session['username']}")
