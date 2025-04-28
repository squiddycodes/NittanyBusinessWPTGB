from flask import Blueprint, render_template, request
import random
import sqlite3 as sql

from pandas.core.interchange.from_dataframe import protocol_df_chunk_to_pandas

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
    email = request.form['email']
    return render_template('productregisterform.html', email = email)

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
def new_product():
    listing_id = request.form['listing_id']
    print("listing_id", listing_id)
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

    newProdTitle = request.form.get('newProdTitle', '').strip()
    print(newProdTitle)
    if not newProdTitle:
        newProdTitle = product[0]

    newProdName = request.form.get('newProdName', '').strip()
    if not newProdName:
        newProdName = product[1]

    newProdDescription = request.form.get('newProdDescription', '').strip()
    if not newProdDescription:
        newProdDescription = product[2]

    newProdCategory = request.form.get('newProdCategory', '').strip()
    if not newProdCategory:
        newProdCategory = product[3]

    newProdQuantity = request.form.get('newProdQuantity', '').strip()
    if not newProdQuantity:
        newProdQuantity = product[4]

    newProdPrice = request.form.get('newProdPrice', '').strip()
    if not newProdPrice:
        newProdPrice = product[5]

    newProdStatus = request.form.get('newProdStatus', '').strip()
    if not newProdStatus:
        newProdStatus = product[6]

    email = request.form['email']
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

@products_bp.route("/AddNewProduct", methods = ['POST', 'GET'])
def add_product():
    newProdTitle = request.form['newProdTitle']
    newProdName = request.form['newProdName']
    newProdDescription = request.form['newProdDescription']
    newProdCategory = request.form['newProdCategory']
    newProdQuantity = request.form['newProdQuantity']
    newProdPrice = request.form['newProdPrice']
    newProdStatus = request.form['newProdStatus']
    email = request.form['email']
    print("email used to create new product: ", email)

    connection = sql.connect('database.db')

    new_id = random.randint(1, 3500)
    unique = False

    cursor = connection.cursor()

    while not unique:
        matching_listid = cursor.execute('SELECT COUNT(*) as rows FROM Product_Listings WHERE Listing_ID = ?', (new_id,))

        if matching_listid.fetchone()[0] <= 0:
            unique = True
        else:
            new_id = random.randint(1, 3500)


    cursor.execute(
        'INSERT INTO Product_Listings (Seller_Email,'
        'Product_Title,'
        'Listing_ID,'
        'Product_Name,'
        'Product_Description,'
        'Category,'
        'Quantity,'
        'Product_Price,'
        'Status) VALUES (?,?,?,?,?,?,?,?,?)', (email,newProdTitle,new_id,newProdName,newProdDescription,newProdCategory,newProdQuantity,newProdPrice,newProdStatus,)
    )
    connection.commit()
    connection.close()


    return render_template('sellersLandingPage.html', email = request.form['email'])

@products_bp.route("/ReviewRequests", methods = ['POST', 'GET'])
def reviewrequests():
    email = request.form['email']

    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT request_id, sender_email, request_type, request_desc FROM Requests WHERE request_status != 1 AND helpdesk_staff_email = ? AND request_type != ?',
        (email, 'HelpDeskRegistration',))
    nonUserRequests = cursor.fetchall()

    cursor.execute(
        'SELECT request_id, sender_email, request_type, request_desc FROM Requests WHERE request_status != 1 AND helpdesk_staff_email = ? AND request_type == ?',
        (email, 'HelpDeskRegistration',))
    UserRequests = cursor.fetchall()
    connection.close()

    return render_template('reviewRequests.html', email = email, nonUserRequests = nonUserRequests, UserRequests=UserRequests)

@products_bp.route("/ReviewRequests/<int:request_id>", methods = ['POST', 'GET'])
def reviewUserrequest(request_id):
    email = ""
    if request.method == 'GET':
        email = request.args.get('email')
    elif request.method == 'POST':
        email = request.form['email']

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT sender_email, request_type, request_desc FROM Requests WHERE request_id = ?', (request_id,))
    UserRequest = cursor.fetchone()
    return render_template('approveAccountCreate.html', email=email, request_id=request_id, UserRequests=UserRequest)

@products_bp.route("/ReturntoHelpDesk", methods = ['POST', 'GET'])
def returntoHelpDesk():
    email = request.form['email']
    return render_template('helpdeskLandingPage.html', email = email)

@products_bp.route("/ApproveAccount", methods = ['POST', 'GET'])
def approveRequest():
    email = request.form['email']
    print(email)
    sender_email = request.form['userID']
    print(sender_email)
    request_id = request.form['requestID']
    print(request_id)
    requestMsg = request.form['requestMsg']
    print(requestMsg)
    requestPos = requestMsg.split(":")[1]
    print(requestPos)

    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE HelpDesk SET Position = ? WHERE email = ?', (requestPos, sender_email,))
    connection.commit()

    cursor.execute('UPDATE Requests SET request_status = 1 WHERE request_id = ?', (request_id,))
    connection.commit()

    cursor.execute(
        'SELECT request_id, sender_email, request_type, request_desc FROM Requests WHERE request_status != 1 AND helpdesk_staff_email = ? AND request_type != ?',
        (email, 'HelpDeskRegistration',))
    nonUserRequests = cursor.fetchall()

    cursor.execute(
        'SELECT request_id, sender_email, request_type, request_desc FROM Requests WHERE request_status != 1 AND helpdesk_staff_email = ? AND request_type == ?',
        (email, 'HelpDeskRegistration',))
    UserRequests = cursor.fetchall()
    connection.close()
    return render_template('reviewrequests.html', email=email, nonUserRequests=nonUserRequests, UserRequests=UserRequests)

@products_bp.route("/ReturntoRequests", methods = ['POST', 'GET'])
def returntoRequests():
    email = request.form['email']
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT request_id, sender_email, request_type, request_desc FROM Requests WHERE request_status != 1 AND helpdesk_staff_email = ? AND request_type != ?',
        (email, 'HelpDeskRegistration',))
    nonUserRequests = cursor.fetchall()

    cursor.execute(
        'SELECT request_id, sender_email, request_type, request_desc FROM Requests WHERE request_status != 1 AND helpdesk_staff_email = ? AND request_type == ?',
        (email, 'HelpDeskRegistration',))
    UserRequests = cursor.fetchall()
    connection.close()
    return render_template('reviewrequests.html', email = email, nonUserRequests = nonUserRequests, UserRequests=UserRequests)