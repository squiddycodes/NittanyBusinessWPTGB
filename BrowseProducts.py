from flask import Flask, Blueprint, render_template, request
import sqlite3 as sql
import hashlib
#from app import create_app

#app = create_app()
BrowseProducts_bp = Blueprint('BrowseProducts', __name__, template_folder='templates')

@BrowseProducts_bp.route('/BrowseProducts', methods=['POST', 'GET']) #PRESS LOG IN
def loadProductsPage():
    email = request.form['email']

    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT Product_Title, Listing_ID, Category, Quantity, Status FROM Product_Listings WHERE Status = 1')
    products = cursor.fetchall()
    connection.close()
    # Fills table with products

    return render_template('productcatalogue.html', email=email, productfile=products)

@BrowseProducts_bp.route('/BuyersHomePage', methods=['POST', 'GET'])
def returntoHomePage():
    email = request.form['email']
    return render_template('buyersLandingPage.html', email = email)

@BrowseProducts_bp.route("/BrowseProducts/<int:listing_id>")
def browse_product(listing_id):
    print(listing_id)
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT Product_Title, Listing_ID, Category, Quantity, Status FROM Product_Listings WHERE Listing_ID = ?', (listing_id,))
    product = cursor.fetchone()
    connection.close()
    print("product", product)
    return render_template("productPage.html", product=product)