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
def showMenu(rest_id):
    restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template(
            'menu.html', rest_id=rest_id, rest_name = restaurant.name, items = items)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'],
            address = request.form['address'],
            phone = request.form['phone'],
            website = request.form['website'])
        session.add(newRestaurant)
        session.commit()
        flash('New Restaurant Added')
        return redirect(url_for('homePage'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurants/<int:rest_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(rest_id):
    editedRestaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        editedRestaurant.name = request.form['name']
        editedRestaurant.address = request.form['address']
        editedRestaurant.phone = request.form['phone']
        editedRestaurant.website = request.form['website']
        session.add(editedRestaurant)
        session.commit()
        flash('Restaurant Sucdessfully Edited')
        return redirect(url_for('homePage'))
    else:
        return render_template('editrestaurant.html', rest_name = editedRestaurant.name,
            rest_address = editedRestaurant.address,
            rest_phone = editedRestaurant.phone,
            rest_website = editedRestaurant.website,
            rest_id = rest_id)

@app.route('/restaurants/<int:rest_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(rest_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        flash('Restaurant Sucdessfully Deleted')
        return redirect(url_for('homePage'))
    else:
        return render_template('deleterestaurant.html', rst_id = rest_id, rest_name = restaurantToDelete.name)

@app.route('/restaurants/<int:rest_id>/new/', methods=['GET', 'POST'])
def newMenuItem(rest_id):
    restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=rest_id)
        session.add(newItem)
        session.commit()
        flash('New Menu Item Added')
        return redirect(url_for('showMenu',rest_id = rest_id))
    else:
        return render_template('newmenu.html',rest_id = rest_id, rest_name = restaurant.name)

@app.route('/restaurants/<int:rest_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(rest_id, menu_id):
    itemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        itemToEdit.name = request.form['name']
        itemToEdit.description = request.form['description']
        itemToEdit.price = request.form['price']
        itemToEdit.course = request.form['course']
        session.add(itemToEdit)
        session.commit()
        flash('Menu Item Sucdessfully Edited')
        return redirect(url_for('showMenu',rest_id = rest_id))
    else:
        return render_template('editmenu.html',
            menu_name = itemToEdit.name,
            menu_description = itemToEdit.description,
            menu_price = itemToEdit.price,
            menu_course = itemToEdit.course,
            rest_id = rest_id,
            menu_id = menu_id)

@app.route('/restaurants/<int:rest_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(rest_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Sucdessfully Deleted')
        return redirect(url_for('showMenu',rest_id = rest_id))
    else:
        return render_template('deletemenu.html', rest_id = rest_id, menu_id = menu_id, menu_name = itemToDelete.name)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        """ newMessage = Message(name = request.form['name'],
            email = request.form['email'],
            subject = request.form['subject'],
            msg = request.form['message'])
        session.add(newMessage)
        session.commit() """
        return redirect(url_for('homePage'))
    else:
        return render_template('contact.html')

# API Endpoints:
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [r.serialize for r in restaurants])

@app.route('/restaurants/<int:rest_id>/menu/JSON/')
def menuJSON(rest_id):
    menuItems = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
    return jsonify(MenuItems = [i.serialize for i in menuItems])

@app.route('/restaurants/<int:rest_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(rest_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = [menuItem.serialize])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
