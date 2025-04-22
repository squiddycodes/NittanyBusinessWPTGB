from flask import Blueprint, render_template, request
import pandas as pd
import sqlite3 as sql

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/MyProducts', methods=['POST', 'GET'])
def loadSellerProducts():
    email = request.form['email']

    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Product_Title, Listing_ID, Category, Quantity, Status FROM Product_Listings WHERE Seller_Email = ?', (email,))
    products = cursor.fetchall()
    connection.close()
    #Fills table with seller's products

    return render_template('sellerproducts.html', email=email, productfile = products)

@products_bp.route('/ProductRegistration', methods=['POST', 'GET'])
def loadProductRegistrar():
    return render_template('productregisterform.html')

@products_bp.route('/SellerHomePage', methods=['POST', 'GET'])
def returntoHomePage():
    email = request.form['email']
    return render_template('sellersLandingPage.html', email = email)