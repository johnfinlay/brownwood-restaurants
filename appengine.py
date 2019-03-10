from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1', 'address': '123 Elm', 'phone': '867-5309', 'website': 'google.com'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1', 'address': '123 Elm', 'phone': '867-5309', 'website': 'google.com'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3', 'address': '123 Elm', 'phone': '867-5309', 'website': 'google.com'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants/')
def homePage():
    return render_template('index.html', restaurants = restaurants)

@app.route('/restaurants/<int:rest_id>/')
def showMenu(rest_id):
    return render_template(
            'menu.html', rest_id=rest_id, rest_name = restaurant['name'], items = items)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        return redirect(url_for('homePage'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurants/<int:rest_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(rest_id):
    if request.method == 'POST':
        return redirect(url_for('homePage'))
    else:
        return render_template('editrestaurant.html', rest_name = restaurant['name'],
            rest_address = restaurant['address'],
            rest_phone = restaurant['phone'],
            rest_website = restaurant['website'])

@app.route('/restaurants/<int:rest_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(rest_id):
    return render_template('deleterestaurant.html', rest_name = restaurant['name'])

@app.route('/restaurants/<int:rest_id>/new/', methods=['GET', 'POST'])
def newMenuItem(rest_id):
     return render_template('newmenu.html', rest_name = restaurant['name'])

@app.route('/restaurants/<int:rest_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(rest_id, menu_id):
    return render_template('editmenu.html',
        menu_name = item['name'],
        menu_description = item['description'],
        menu_price = item['price'],
        menu_course = item['course'])

@app.route('/restaurants/<int:rest_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(rest_id, menu_id):
    return 'Delete Menu Item'

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
