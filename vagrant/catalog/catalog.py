from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from sqlalchemy import desc

from flask import session as login_session
# to generate state token
import random, string

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    return 'The current session state is: {}'.format(login_session['state'])

# home page to display all categories and the last few added items
@app.route('/')
@app.route('/catalog')
def show_catalog():
    categories = session.query(Category).all()
    items_to_show = 10
    items = \
        session.query(Item). \
        order_by(desc(Item.id)). \
        limit(items_to_show).all()
    return render_template('catalog.html', categories=categories, items=items)


# category page to display one category with all its items
@app.route('/catalog/<category_name>')
# @app.route('/catalog/<category_name>>/items')
def show_category(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('show_category.html', category=category, items=items)


# new item page for adding new items to catalog
@app.route('/catalog/items/create', methods=['GET', 'POST'])
@app.route('/catalog/<category_name>/items/create', methods=['GET', 'POST'])
def create_item(category_name=''):
    if request.method == 'POST':
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'])
        session.add(new_item)
        session.commit()
        # Get category name form database
        # even if there was one in the url, user could have changed it
        category = session.query(Category).filter_by(id = request.form['category']).one()
        flash('New catalog item created!')
        return redirect(url_for('show_category',
            category_name = category.name))
    else:
        categories = session.query(Category).all()
        return render_template(
            'create_item.html',
            categories=categories, category_name=category_name)


# edit item page to edit specific item
@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(name=item_name).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.category_id = request.form['category']
        session.add(item)
        session.commit()
        flash('Catalog item is updated!')
        return redirect(url_for('show_category', category_name=item.category.name))
    else:
        return render_template('edit_item.html',
            categories=categories, item=item)


# Delete item
@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    # Save name of category for redirect
    category_name = item.category.name
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Catalog item is deleted!')
        return redirect(url_for('show_category', category_name=category_name))
    else:
        return render_template('delete_item.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
