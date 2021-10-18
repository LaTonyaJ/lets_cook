# lets_cook
## Capstone Project 1
[API Link](https://www.themealdb.com/api.php "The MealDB")

* My app is named **Lets's Cook**
* [Go to my app](https://lj-lets-cook.herokuapp.com/)

My app is a random recipe generator with the ability to save your favorite meals. The navbar has a logo. This logo is how you generate a new random recipe. You can also filter the search by submitting a category.
I chose this functionality to narrow the randomness to your own liking but also get a new recipe you've possibly never tried. 
If the category is available, a recipe for that category is displayed, if the category is not valid then you get a random recipe. 
To save favorites you have to create an account and log in.
Creating your own CookBook is just a small bonus for the recipes you want to save for later, favorites can be removed as well, maybe you didn't like that one. I chose this functionality to implement some authentication. 

---

### User Flow

1. Navigate to [Lets Cook](https://lj-lets-cook.herokuapp.com/)
1. You should immediately get a random recipe
1. If you want to create a cook book, go ahead and create an account, the login link is in the navbar
1. If not, click **Lets Cook** in the navbar to get a new recipe
1. Want to narrow the search? Add a category....click Filter
    * If your category is valid you should get a new recipe from your chosen category
    * If not, you will get another random recipe
1. Add a recipe to your cookbook by clicking the heart beside the recipe name
1. If you are **NOT** logged in, you will get an error message..
1. Logged in users will be redirected to their cookbook where they can see thumbnails of all their favorites.
    * Clicking an image takes you to the full recipe
    * To remove meals from favorites click [Remove]()

---

### My Stack

**Technologies used:**

* Python
* SQLAlchemy
* Postgresql
* Flask
* WTForms
* Javascript
* Heroku
* SQL
* HTML
* CSS
