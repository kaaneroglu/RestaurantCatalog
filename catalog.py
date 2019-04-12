from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Cuisine, Restaurant
app = Flask(__name__)


engine = create_engine('sqlite:///yycrestaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Route for READ all cuisines
@app.route('/')
@app.route('/cuisines', methods=['GET'])
def showCuisines():
    cuisines= session.query(Cuisine).all()
    return render_template('index.html', title='Restaurant Catalog', cuisines=cuisines)

# Route for CREATE new cuisine
@app.route('/cuisines/new/', methods=['GET', 'POST'])
def newCuisine():
    if request.method == 'POST':
        return "Create new cuisine"
    else:
        return "This page will have a form to take input cuisine name and create that"

# Route for UPDATE cuisine
@app.route('/cuisines/<int:cuisine_id>/edit/', methods=['GET', 'POST'])
def editCuisine(cuisine_id):
    if request.method == 'POST':
        return "This page will edit cuisine %s" % cuisine_id
    else:
        return "This page will edit cuisine %s" % cuisine_id

# Route for DELETE cuisine
@app.route('/cuisines/<int:cuisine_id>/delete/', methods=['GET', 'POST'])
def deleteCuisine(cuisine_id):
    if request.method == 'POST':
        return "This page will delete cuisine %s" % cuisine_id
    else:
        return "This page will delete cuisine %s also need a cancel link to go back to /cuisines" % cuisine_id

# Route for READ all restaurants under a specific cuisine
@app.route('/cuisines/<int:cuisine_id>/', methods=['GET'])
@app.route('/cuisines/<int:cuisine_id>/restaurant/', methods=['GET'])
def showRestaurants(cuisine_id):
    return "This page shows all restaurants for cuisine %s" % cuisine_id

# Route for CREATE new restaurant


@app.route(
    '/cuisines/<int:cuisine_id>/restaurant/new/',
    methods=[
        'GET',
        'POST'])
def newRestaurant(cuisine_id):
    if request.method == 'POST':
        return "Create new restaurant"
    else:
        return "Create new restaurant under cuisine %s" % cuisine_id

# Route for UPDATE restaurant


@app.route(
    '/cuisines/<int:cuisine_id>/restaurant/<int:restaurant_id>/edit/',
    methods=[
        'GET',
        'POST'])
def editRestaurant(cuisine_id, restaurant_id):
    if request.method == 'POST':
        return "This page will edit restaurant %s under cuisine %s" % (
            restaurant_id, cuisine_id)
    else:
        return "This page will edit restaurant %s under cuisine %s" % (
            restaurant_id, cuisine_id)

# Route for DELETE restaurant


@app.route(
    '/cuisines/<int:cuisine_id>/restaurant/<int:restaurant_id>/delete/',
    methods=[
        'GET',
        'POST'])
def deleteRestaurant(cuisine_id, restaurant_id):
    if request.method == 'POST':
        return "This page will delete restaurant %s under cuisine %s" % (
            restaurant_id, cuisine_id)
    else:
        return "This page will delete restaurant %s under cuisine %s" % (
            restaurant_id, cuisine_id)

# JSON API endpoint for getting all restaurants under a cuisine
@app.route('/cuisines/<int:cuisine_id>/restaurant/JSON')
def cuisineRestaurantsJSON(cuisine_id):
    return "This page will have JSON output for all restaurants under cuisine %s" % cuisine_id

# JSON API endpoint for getting a restaurant
@app.route('/cuisines/<int:cuisine_id>/restaurant/<int:restaurant_id>/JSON')
def restaurantDetaisJSON(cuisine_id, restaurant_id):
    return "This page will have JSON output for restaurant %s details under cuisine %s" % (
        restaurant_id, cuisine_id)


if __name__ == '__main__':
    # app.secret_key = 'super_Secret_key' #create sessions
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
