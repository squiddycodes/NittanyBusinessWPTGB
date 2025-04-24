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

@products_bp.route("/MyProducts/EditProduct/<string:email>Editing<int:listing_id>", methods=['POST', 'GET'])
def edit_product(email, listing_id):
    print("Hello World")
    #email = request.form['email']
    print(listing_id)
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT Product_Title, '
        'Product_Name, '
        'Product_Description, '
        'Category, '
        'Quantity, '
        'Product_Price, '
        'Status FROM Product_Listings WHERE Listing_ID = ?', (listing_id,))
    product = cursor.fetchone()
    connection.close()
    print("product", product)
    return render_template("editproduct.html", product=product, listing_id=listing_id, email = email)

@products_bp.route("/UpdateProduct", methods = ['POST', 'GET'])
def update_product():
    listing_id = request.form['listing_id']
    newProdTitle = request.form['newProdTitle']
    newProdName = request.form['newProdName']
    newProdDescription = request.form['newProdDescription']
    newProdCategory = request.form['newProdCategory']
    newProdQuantity = request.form['newProdQuantity']
    newProdPrice = request.form['newProdPrice']
    newProdStatus = request.form['newProdStatus']
    email = request.form['email']
    print("listing_id to be updated: ", listing_id)
    print("email", email)
    connection = sql.connect('database.db')

    cursor = connection.cursor()

    cursor.execute(
        'UPDATE Product_Listings SET Product_Title = ?,'
        'Product_Name = ?,'
        'Product_Description = ?,'
        'Category = ?,'
        'Quantity = ?,'
        'Product_Price = ?,'
        'Status = ? WHERE Listing_ID = ?', (newProdTitle,newProdName,newProdDescription,newProdCategory,newProdQuantity,newProdPrice,newProdStatus,listing_id,)
    )
    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT Product_Title, Listing_ID, Category, Quantity, Status FROM Product_Listings WHERE Seller_Email = ?',
        (email,))
    products = cursor.fetchall()
    connection.close()

    return render_template('sellerproducts.html', email = request.form['email'], productfile = products)