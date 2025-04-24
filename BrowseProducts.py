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
        'SELECT P.Product_Title, P.Listing_ID, P.Category, P.Quantity '
        'FROM Product_Listings AS P '
        'WHERE P.Status = 1 AND (P.Category=? OR P.Category IN (SELECT C.category_name FROM Categories AS C WHERE C.parent_category=?))',("Root","Root"))#get all products in category or child
    products = cursor.fetchall()

    cursor.execute('SELECT category_name FROM Categories WHERE parent_category="Root"')
    subCats = cleanCategories(cursor.fetchall())
    connection.close()
    # Fills table with products

    return render_template('productcatalogue.html', email=email, productfile=products, currCategory="Root", subcategories=subCats, keywords = ("", "Product_Name", "Listing_ID", "Quantity"))

@BrowseProducts_bp.route('/BuyersHomePage', methods=['POST', 'GET'])
def returntoHomePage():
    email = ""
    if request.method == 'GET':
        email = request.args.get('email')
    elif request.method == 'POST':
        email = request.form['email']

    return render_template('buyersLandingPage.html', email = email)

@BrowseProducts_bp.route("/BrowseProducts/<int:listing_id>", methods=['POST'])
def browse_product(listing_id):
    #print(listing_id)
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT Seller_Email, '
        'Product_Title, '
        'Product_Name, '
        'Product_Description, '
        'Category, '
        'Product_Price, '
        'Quantity FROM Product_Listings WHERE Listing_ID = ?', (listing_id,))
    product = cursor.fetchone()
    connection.close()
    #print("product", product)
    return render_template("productPage.html", email=request.form['email'], product=product)

@BrowseProducts_bp.route("/BrowseProducts/<string:currCategory>", methods=['GET', 'POST'])
def browse_products(currCategory):
    if request.method == 'POST':
        #selected = request.form['dropdown']
        selected = request.form.get('dropdown')
        keyword = request.form.get('keywordmenu')
        keywordInput = request.form.get('KeywordInput')
        if selected:
            if keyword:
                return redirect(url_for('BrowseProducts.browse_products', currCategory=selected,email=request.form.get('email'), keyword=keyword, keywordInput=keywordInput))
            else:
                return redirect(url_for('BrowseProducts.browse_products', currCategory=selected, email=request.form.get('email'),keyword="", keywordInput=""))
        else:
            if keyword:
                return redirect(url_for('BrowseProducts.browse_products', currCategory=currCategory, email=request.form.get('email'), keyword=keyword, keywordInput=keywordInput))
            else:
                return redirect(url_for('BrowseProducts.browse_products', currCategory=currCategory, email=request.form.get('email'), keyword="", keywordInput=""))
    elif request.method == 'GET':
        email = request.args.get('email')
        keyword = request.args.get('keyword')
        keywordInput = request.args.get('keywordInput')
        validSpecifiers = ("", "Product_Name", "Listing_ID", "Quantity")
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        products = ''

        if keyword == "":
            cursor.execute(
                'SELECT P.Product_Title, P.Listing_ID, P.Category, P.Quantity '
                'FROM Product_Listings AS P '
                'WHERE P.Status = 1 AND (P.Category=? OR P.Category IN (SELECT C.category_name FROM Categories AS C WHERE C.parent_category=?))',
                (currCategory, currCategory))  # get all products in category or child
            products = cursor.fetchall()
        elif keyword == "Product_Name":
            cursor.execute(
                'SELECT P.Product_Title, P.Listing_ID, P.Category, P.Quantity '
                'FROM Product_Listings AS P '
                'WHERE P.Status = 1 AND P.Product_Title = ? AND (P.Category=? OR P.Category IN (SELECT C.category_name FROM Categories AS C WHERE C.parent_category=?))',
                (keywordInput, currCategory, currCategory))  # get all products in category or child
            products = cursor.fetchall()
        elif keyword == "Listing_ID":
            cursor.execute(
                'SELECT P.Product_Title, P.Listing_ID, P.Category, P.Quantity '
                'FROM Product_Listings AS P '
                'WHERE P.Status = 1 AND P.Listing_ID = ? AND (P.Category=? OR P.Category IN (SELECT C.category_name FROM Categories AS C WHERE C.parent_category=?))',
                (keywordInput, currCategory, currCategory))  # get all products in category or child
            products = cursor.fetchall()
        elif keyword == "Quantity":
            cursor.execute(
                'SELECT P.Product_Title, P.Listing_ID, P.Category, P.Quantity '
                'FROM Product_Listings AS P '
                'WHERE P.Status = 1 AND P.Quantity = ? AND (P.Category=? OR P.Category IN (SELECT C.category_name FROM Categories AS C WHERE C.parent_category=?))',
                (keywordInput, currCategory, currCategory))  # get all products in category or child
            products = cursor.fetchall()

        cursor.execute('SELECT category_name FROM Categories WHERE parent_category=?',(currCategory,))
        subCats = cleanCategories(cursor.fetchall())
        connection.close()
        return render_template('productcatalogue.html', email=email, productfile=products, currCategory=currCategory,
                               subcategories=subCats, keywords = validSpecifiers)

@BrowseProducts_bp.route("/BrowseProducts/Back/<string:currCategory>", methods=['GET', 'POST'])
def backToParentCategory(currCategory):#look for parent and go there
    #get parent of currCategory, reroute to browse_products
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT parent_category FROM Categories WHERE category_name=?', (currCategory,))
    parentCategory = cursor.fetchone()
    connection.close()
    if parentCategory:
        parentCategory = cleanCategories(parentCategory)
        return redirect(url_for('BrowseProducts.browse_products', currCategory=parentCategory[0] , email=request.form.get('email'), keyword="", keywordInput=""))
    else:
        return redirect(
            url_for('BrowseProducts.browse_products', currCategory=currCategory, email=request.form.get('email'), keyword="", keywordInput=""))

def cleanCategories(categories):
    out = []
    for category in categories:
        category = str(category)
        category = category.replace('(\'', '')
        category = category.replace('\',)', '')
        out.append(category)
    return out