#!/usr/bin/env python3
#
# Restaurant catalog for Calgary

from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Cuisine, Restaurant


from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


engine = create_engine('sqlite:///yycrestaurants.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Route for login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print ("Done!")
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        #return response
        flash("you are now logged out")
        return redirect(url_for('showCuisines'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Route for READ all cuisines
@app.route('/')
@app.route('/cuisines', methods=['GET'])
def showCuisines():
    cuisines = session.query(Cuisine).all()
    return render_template('index.html', title='Restaurant Catalog', cuisines=cuisines, login_session=login_session)

# Route for CREATE new cuisine
@app.route('/cuisines/new/', methods=['GET', 'POST'])
def newCuisine():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCuisineName = Cuisine(name=request.form['name'])
        session.add(newCuisineName)
        session.commit()
        flash("New cuisine created!")
        return redirect(url_for('showCuisines'))
    else:
        cuisines = session.query(Cuisine).all()
        return render_template('createcuisine.html', title='Restaurant Catalog', cuisines=cuisines, login_session=login_session)

# Route for UPDATE cuisine
@app.route('/cuisines/<int:cuisine_id>/edit/', methods=['GET', 'POST'])
def editCuisine(cuisine_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        return "This page will edit cuisine %s" % cuisine_id
    else:
        return "This page will edit cuisine %s" % cuisine_id

# Route for DELETE cuisine
@app.route('/cuisines/<int:cuisine_id>/delete/', methods=['GET', 'POST'])
def deleteCuisine(cuisine_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        return "This page will delete cuisine %s" % cuisine_id
    else:
        return "This page will delete cuisine %s also need a cancel link to go back to /cuisines" % cuisine_id

# Route for READ all restaurants under a specific cuisine
@app.route('/cuisines/<int:cuisine_id>/', methods=['GET'])
@app.route('/cuisines/<int:cuisine_id>/restaurant/', methods=['GET'])
def showRestaurants(cuisine_id):
    cuisines = session.query(Cuisine).all()
    cuisineName  = session.query(Cuisine).filter_by(id=cuisine_id).one()
    restaurants = session.query(Restaurant).filter_by(cuisine_id=cuisine_id)
    return render_template('restaurants.html', title='Restaurant Catalog', cuisines=cuisines, restaurants=restaurants, cuisineName=cuisineName, login_session=login_session)

# Route for CREATE new restaurant
@app.route(
    '/cuisines/<int:cuisine_id>/restaurant/new/',
    methods=[
        'GET',
        'POST'])
def newRestaurant(cuisine_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newRestaurantInfo = Restaurant(name = request.form['name'], description = request.form['description'], phone = request.form['phone'], website = request.form['website'], address = request.form['address'], cuisine_id = cuisine_id)
        session.add(newRestaurantInfo)
        session.commit()
        flash("New restaurant created!")
        return redirect(url_for('showRestaurants',cuisine_id = cuisine_id))
    else:
        cuisines = session.query(Cuisine).all()
        cuisineName = session.query(Cuisine).filter_by(id=cuisine_id).one()
        return render_template('createrestaurant.html', cuisine_id = cuisine_id, title='Restaurant Catalog', cuisines=cuisines, cuisineName=cuisineName, login_session=login_session)

# Route for UPDATE restaurant
@app.route(
    '/cuisines/<int:cuisine_id>/restaurant/<int:restaurant_id>/edit/',
    methods=[
        'GET',
        'POST'])
def editRestaurant(cuisine_id, restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        if request.form['description']:
            editedRestaurant.description = request.form['description']
        if request.form['phone']:
            editedRestaurant.phone = request.form['phone']
        if request.form['website']:
            editedRestaurant.website = request.form['website']
        if request.form['address']:
            editedRestaurant.address = request.form['address']
        session.commit()
        flash("Restaurant has been updated!")
        return redirect(url_for('showRestaurants', cuisine_id = cuisine_id))
    else:
        cuisines = session.query(Cuisine).all()
        cuisineName = session.query(Cuisine).filter_by(id=cuisine_id).one()
        return render_template('editrestaurant.html', cuisine_id=cuisine_id, restaurant_id=restaurant_id, editedRestaurant=editedRestaurant, cuisineName=cuisineName, cuisines=cuisines, login_session=login_session)

# Route for DELETE restaurant
@app.route(
    '/cuisines/<int:cuisine_id>/restaurant/<int:restaurant_id>/delete/',
    methods=[
        'GET',
        'POST'])
def deleteRestaurant(cuisine_id, restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash("Restaurant {} is deleted".format(deletedRestaurant.name))
        return redirect(url_for('showRestaurants', cuisine_id = cuisine_id))
    else:
        cuisines = session.query(Cuisine).all()
        cuisineName = session.query(Cuisine).filter_by(id=cuisine_id).one()
        return render_template('deleterestaurant.html', cuisine_id = cuisine_id, cuisines=cuisines, cuisineName=cuisineName, deletedrestaurant=deletedRestaurant, login_session=login_session)

# JSON API endpoint for getting all restaurants under a cuisine
@app.route('/cuisines/<int:cuisine_id>/JSON')
def cuisineRestaurantsJSON(cuisine_id):
    restaurants = session.query(Restaurant).filter_by(cuisine_id=cuisine_id)
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

# JSON API endpoint for getting a restaurant
@app.route('/cuisines/<int:cuisine_id>/restaurant/<int:restaurant_id>/JSON')
def restaurantDetaisJSON(cuisine_id, restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(Restaurants = restaurant.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_Secret_key' #create sessions
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
