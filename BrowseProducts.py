from flask import Flask, Blueprint, render_template, request, url_for, redirect
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
        'SELECT P.Product_Title, P.Listing_ID, P.Category, P.Quantity, P.Status '
        'FROM Product_Listings AS P '
        'WHERE P.Status = 1 AND (P.Category=? OR P.Category IN (SELECT C.category_name FROM Categories AS C WHERE C.parent_category=?))',("Root","Root"))#get all products in category or child
    products = cursor.fetchall()

    cursor.execute('SELECT category_name FROM Categories WHERE parent_category="Root"')
    subCats = cleanCategories(cursor.fetchall())
    connection.close()
    # Fills table with products

    return render_template('productcatalogue.html', email=email, productfile=products, currCategory="Root", subcategories=subCats)

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

@BrowseProducts_bp.route("/BrowseProducts/<string:currCategory>", methods=['GET', 'POST'])
def browse_products(currCategory):
    if request.method == 'POST':
        selected = request.form['dropdown']
        return redirect(url_for('BrowseProducts.browse_products', currCategory=selected,email=request.form.get('email')))
    elif request.method == 'GET':
        email = request.args.get('email')
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            'SELECT P.Product_Title, P.Listing_ID, P.Category, P.Quantity, P.Status '
            'FROM Product_Listings AS P '
            'WHERE P.Status = 1 AND (P.Category=? OR P.Category IN (SELECT C.category_name FROM Categories AS C WHERE C.parent_category=?))',
            (currCategory, currCategory))  # get all products in category or child
        products = cursor.fetchall()

        cursor.execute('SELECT category_name FROM Categories WHERE parent_category=?',(currCategory,))
        subCats = cleanCategories(cursor.fetchall())
        connection.close()
        return render_template('productcatalogue.html', email=email, productfile=products, currCategory=currCategory,
                               subcategories=subCats)

def cleanCategories(categories):
    out = []
    for category in categories:
        category = str(category)
        category = category.replace('(\'', '')
        category = category.replace('\',)', '')
        out.append(category)
    return out