from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Category, Item, User
from sqlalchemy import desc
# Import for session management and to generate state token
from flask import session as login_session
import random
import string
# Import for server side login
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from sqlalchemy import inspect


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    print('state in login_session: {}'.format(login_session['state']))
    print('state received from client: {}'.format(request.args.get('state')))
    # Check if token sent by client is the same as token sent by server
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # If client has the right state token collect one-time code
    code = request.data
    print('state token received is OK')

    # Try exchanging one-time code to credentails object
    # credential object will have the access token
    print('Trying to exchange one-time code for credentils')
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # Store received access token
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade to authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if received access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
           .format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If access token is not valid abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error'), 500))
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if acces token is for the intended user
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(json.dumps(
            'Token\'s user id does not match given user id.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            'Token\'s client id does not match app\'s'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(json.dumps(
            'Current user is already logged in.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store access_token and google_id if user was not logged in
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get info about user from google
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    # print('Printing answer')
    # print(answer)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user is already in database
    user_id = get_user_id(login_session['email'])
    # Create user if needed
    if user_id is None:
        user_id = create_user(login_session)
    # Store user's id in login_session
    login_session['user_id'] = user_id
    print('User {} is succesfully logged in'.format(login_session['email']))

    output = '''
        <h1>Welcome {} !</h1>
        <img
            src = "{}"
            style = "width: 300px; height: 300px;
                    border-radius: 150px;-webkit-border-radius: 150px;
                    -moz-border-radius: 150px;"
        >
        '''.format(login_session['username'], login_session['picture'])
    return output


def create_user(login_session):
    # Add user to database
    user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(user)
    session.commit()
    # Return new user's id
    new_user = session.query(User).filter_by(
        email=login_session['email']).one()
    print('User: {} is created with id: {}'.format(
        login_session['email'], new_user.id))
    return new_user.id


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def get_user():
    # Check if user is logged in
    # print('Cheking if user email is in login_session')
    user = login_session.get('email')
    print('==> Email in login_session is: {}'.format(user))
    # If user is logged in get user info
    if user is not None:
        user = session.query(User).filter_by(
            email=login_session['email']).one()
    return user


# Logout user: remove access_token, reset login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    # If there is no access_token in login_session abort
    if access_token is None:
        print('access_token is None')
        response = make_response(json.dumps(
            'Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnet access_token is: {}'.format(access_token))
    print('In gconnect user email is: {}'.format(login_session['email']))

    # Revoke access_token from user
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # If revoke was succesfull, clear login_session information
    if result['status'] == '200':
        print('User {} is succesfully logged out'.format(login_session['email']))
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return redirect(url_for('show_catalog'))
    # If not lot error, and clear login-session
    else:
        # Log failure to revoke token
        print('Failed to revoke token from user')
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return redirect(url_for('show_catalog'))


# JSON endpoint for catalog
@app.route('/catalog.json')
def catalog_JSON():
    categories = session.query(Category).all()
    catalog=[category.serialize for category in categories]
    for category in catalog:
        items = session.query(Item).filter_by(category_id=category['id']).all()
        category['items'] = [item.serialize for item in items]
    print(catalog)
    return jsonify(Catalog=catalog)


# JSON endpoint for category
@app.route('/catalog/<category_name>.json')
def category_JSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return jsonify(category_items=[item.serialize for item in items])


# JSON endpoint for item
@app.route('/catalog/<category_name>/<item_name>.json')
def item_JSON(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    return jsonify(item=[item.serialize])


# Home page to display all categories and the last few added items
@app.route('/')
@app.route('/catalog')
def show_catalog():
    # Get all categories
    categories = session.query(Category).all()
    # Limit items shown to:
    items_to_show = 10
    # Get the last "items_to_show" items added
    items = \
        session.query(Item). \
        order_by(desc(Item.id)). \
        limit(items_to_show).all()
    # Get current user
    user = get_user()
    return render_template(
        'catalog.html', categories=categories, items=items, user=user)


# Category page to display one category with all its items
@app.route('/catalog/<category_name>')
def show_category(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    user = get_user()
    return render_template(
        'show_category.html', category=category, items=items, user=user)


# Item page to display one item
@app.route('/catalog/<category_name>/<item_name>/<item_id>')
def show_item(category_name, item_name, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    user = get_user()
    print('Showing {} in {}'.format(
        item.name, item.category.name))
    return render_template(
        'show_item.html', category_name=category_name, item=item, user=user)

# New item page for adding new items to catalog
@app.route('/catalog/items/create', methods=['GET', 'POST'])
@app.route('/catalog/<category_name>/items/create', methods=['GET', 'POST'])
def create_item(category_name=''):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # Check if item is valid
        # Check if name field is filled out
        if request.form['name'] == '':
            flash('Item not created. Cannot create item without a name')
            return redirect(url_for('show_catalog'))
        # Check if name is uniqe in category
        name_count = session.query(Item).filter(
            Item.name==request.form['name'],
            Item.category_id==request.form['category']).count()
        # Send error message if the name is already exists in the category
        if name_count > 0:
            flash('Item not created. Category already has an item with the name selected.')
            return redirect(url_for('show_catalog'))
        # Create new item if input data was all right
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'],
            user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()
        # Get category name form database
        # even if there was one in the url, user could have changed it
        category = session.query(Category).filter_by(
            id=request.form['category']).one()
        flash('New catalog item created!')
        return redirect(url_for('show_category',
                                category_name=category.name))
    else:
        categories = session.query(Category).all()
        user = get_user()
        return render_template(
            'create_item.html',
            categories=categories, category_name=category_name, user=user)


# edit item page to edit specific item
@app.route('/catalog/<category_name>/<item_name>/<item_id>/edit', methods=['GET', 'POST'])
def edit_item(category_name, item_name, item_id):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.category_id = request.form['category']
        session.add(item)
        session.commit()
        flash('Catalog item is updated!')
        return redirect(url_for('show_category',
                                category_name=item.category.name))
    else:
        user = get_user()
        return render_template('edit_item.html',
                               categories=categories, item=item, user=user)


# Delete item page
@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    # item = session.query(Item).join(Category).\
    #         filter(Item.name==item_name, Category.name==category_name).one()
    item = session.query(Item).filter(Item.name==item_name).one()
    if request.method == 'POST':
        # Save name of category for redirect
        category_name = item.category.name
        # Delete item
        session.delete(item)
        session.commit()
        # Flash message about succesful deletion
        flash('Catalog item is deleted!')
        # Redirect to Category page
        return redirect(url_for('show_category', category_name=category_name))
    else:
        user = get_user()
        return render_template('delete_item.html', item=item, user=user)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)

# TO DO:
# - do not let user enter empty items
# - if going to new item from catalog return to catalog
# - style login page
# - when closing show-item go back where you came from? 
#   (it always goes back to category) should it go back to catalog?
# - show_catalog.html doesn't display category