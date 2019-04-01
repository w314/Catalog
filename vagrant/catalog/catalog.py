from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from sqlalchemy import desc

app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


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
@app.route('/catalog/categories/<int:category_id>')
@app.route('/catalog/categories/<int:category_id>/items')
def show_category(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('show_items.html', category=category, items=items)


# new item page for adding new items to catalog
@app.route('/catalog/items/new', methods=['GET', 'POST'])
@app.route('/catalog/categories/<int:category_id>/items/new')
def create_item(category_id=-1):
    if request.method == 'POST':
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'])
        session.add(new_item)
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        # Get category name based on category_id if provided by url
        category_name = '' if (category_id == -1) else \
            session.query(Category).filter_by(id=category_id).one().name
        categories = session.query(Category).all()
        return render_template(
            'new_item.html',
            categories=categories, category_name=category_name)


# edit item page to edit specific item
@app.route('/catalog/items/<int:item_id>/edit')
def edit_item(item_id):
    return 'edit item'


# delete item page to delete specific item
@app.route('/catalog/items/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('show_category', category_id=item.category_id))
    else:
        return render_template('delete_item.html', item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
