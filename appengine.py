from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def homePage():
    restaurants = session.query(Restaurant).all()
    return render_template('index.html', restaurants = restaurants)

@app.route('/restaurants/<int:rest_id>/')
def showRestaurant(rest_id):
    return 'Restaurant Page will display menu items.'
""" def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template(
            'menu.html', restaurant_id=restaurant_id, restaurant_name = restaurant.name, items = items) """

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    return 'New Restaurant Page'

@app.route('/restaurants/<int:rest_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(rest_id):
    return 'Edit Restaurant'

@app.route('/restaurants/<int:rest_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(rest_id):
    return 'Delete Restaurant'

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
     return 'New Menu Item'
""" if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                            'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New Menu Item Created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id) """



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    return 'Edit Menu Item'
"""editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
if request.method == 'POST':
    if request.form['name']:
        editedItem.name = request.form['name']
    session.add(editedItem)
    session.commit()
    flash('Menu Item Edited!')
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
else:
    return render_template(
        'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem) """

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    return 'Delete Menu Item'
"""     itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Deleted!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html', item=itemToDelete) """

@app.route('/about')
def about():
    return 'About Us Coming Soon...'

@app.route('/contact')
def contact():
    return 'Contact Us Coming Soon...'

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
