from flask import Flask, render_template, request, redirect, url_for #redirect used in routeToPage, for dropdown ease of access
import os
import pandas as pd
import sqlite3 as sql
import hashlib

from werkzeug.serving import connection_dropped_errors

# Derek Guidorizzi, Joe Long, Nicole Chen, Bhavishya Malla
# We've Played these Games Before
# CMPSC 431W Section 1
# Nittany Business Phase 2 Demo

def createDB():
    connection = sql.connect('database.db')
    connection.execute('CREATE TABLE IF NOT EXISTS Users(email TEXT PRIMARY KEY, password TEXT NOT NULL);')
    connection.execute('CREATE TABLE IF NOT EXISTS Address(address_id TEXT, zipcode INTEGER, street_num INTEGER, street_name TEXT, PRIMARY KEY(address_ID));')
    connection.execute('CREATE TABLE IF NOT EXISTS Buyers(email TEXT, business_name TEXT, buyer_address_id TEXT, PRIMARY KEY(email));')
    connection.execute('CREATE TABLE IF NOT EXISTS Categories(parent_category TEXT, category_name TEXT, PRIMARY KEY(category_name));')
    connection.execute('CREATE TABLE IF NOT EXISTS Credit_Cards(credit_card_num TEXT, card_type TEXT, expire_month INTEGER, expire_year INTEGER, security_code INTEGER, Owner_Email TEXT, PRIMARY KEY(credit_card_num));')
    connection.execute('CREATE TABLE IF NOT EXISTS HelpDesk(email TEXT, Position TEXT, PRIMARY KEY(email));')
    connection.execute('CREATE TABLE IF NOT EXISTS Orders(Order_ID INTEGER, Seller_Email TEXT, Listing_ID INTEGER, Buyer_Email TEXT, Date TEXT, Quantity INTEGER, Payment INTEGER, PRIMARY KEY(Order_ID));')
    connection.execute('CREATE TABLE IF NOT EXISTS Product_Listings(Seller_Email TEXT, Listing_ID INTEGER, Category TEXT, Product_Title TEXT, Product_Name TEXT, Product_Description TEXT, Quantity INTEGER, Product_Price TEXT, Status INTEGER, PRIMARY KEY(Seller_Email, Listing_ID));')
    connection.execute('CREATE TABLE IF NOT EXISTS Requests(request_id INTEGER, sender_email TEXT, helpdesk_staff_email TEXT, request_type TEXT, request_desc TEXT, request_status INTEGER, PRIMARY KEY(request_id));')
    connection.execute('CREATE TABLE IF NOT EXISTS Reviews(Order_ID INTEGER, Rate INTEGER, Review_Desc TEXT, PRIMARY KEY(Order_ID));')
    connection.execute('CREATE TABLE IF NOT EXISTS Sellers(email TEXT, business_name TEXT, Business_Address_ID TEXT, bank_routing_number TEXT, bank_account_number INTEGER, balance INTEGER, PRIMARY KEY(email));')
    connection.execute('CREATE TABLE IF NOT EXISTS Zipcode_Info(zipcode INTEGER, city TEXT, state TEXT, PRIMARY KEY(zipcode));')

def hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

def insertUsers():
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Users_path = os.path.join('NittanyBusinessDataset_v3', 'Users.csv')

    Usersdata = pd.read_csv(Users_path)

    for _, row in Usersdata.iterrows():
        Email = row['email']
        password = row['password']
        hashedPW = hash(password)

        cursor.execute('''INSERT OR IGNORE INTO Users (email, password) VALUES (?, ?)''', (Email, hashedPW))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Address_path = os.path.join('NittanyBusinessDataset_v3', 'Address.csv')

    Addressdata = pd.read_csv(Address_path)

    for _, row in Addressdata.iterrows():
        addrID = row['address_id']
        zipcode = row['zipcode']
        streetnum = row['street_num']
        streetname = row['street_name']

        cursor.execute('''INSERT OR IGNORE INTO Address (address_id, zipcode, street_num, street_name) VALUES (?, ?, ?, ?)''', (addrID, zipcode, streetnum, streetname))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Buyers_path = os.path.join('NittanyBusinessDataset_v3', 'Buyers.csv')

    Buyersdata = pd.read_csv(Buyers_path)

    for _, row in Buyersdata.iterrows():
        Email = row['email']
        businessname = row['business_name']
        buyeraddrID = row['buyer_address_id']

        cursor.execute('''INSERT OR IGNORE INTO Buyers (email, business_name, buyer_address_id) VALUES (?, ?, ?)''', (Email, businessname, buyeraddrID))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Categories_path = os.path.join('NittanyBusinessDataset_v3', 'Categories.csv')

    Categoriesdata = pd.read_csv(Categories_path)

    for _, row in Categoriesdata.iterrows():
        parentCategory = row['parent_category']
        categoryname = row['category_name']

        cursor.execute('''INSERT OR IGNORE INTO Categories (parent_category, category_name) VALUES (?, ?)''', (parentCategory, categoryname))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Credit_Cards_path = os.path.join('NittanyBusinessDataset_v3', 'Credit_Cards.csv')

    Credit_Cardsdata = pd.read_csv(Credit_Cards_path)

    for _, row in Credit_Cardsdata.iterrows():
        ccardnum = row['credit_card_num']
        ccardtype = row['card_type']
        expire_month = row['expire_month']
        expire_year = row['expire_year']
        seccode = row['security_code']
        Email = row['Owner_email']

        cursor.execute('''INSERT OR IGNORE INTO Credit_Cards (credit_card_num, card_type, expire_month, expire_year, security_code, Owner_email) VALUES (?, ?, ?, ?, ?, ?)''', (ccardnum, ccardtype, expire_month, expire_year, seccode, Email))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    HelpDesk_path = os.path.join('NittanyBusinessDataset_v3', 'HelpDesk.csv')

    HelpDeskdata = pd.read_csv(HelpDesk_path)

    for _, row in HelpDeskdata.iterrows():
        Email = row['email']
        position = row['Position']

        cursor.execute('''INSERT OR IGNORE INTO HelpDesk (email, Position) VALUES (?, ?)''', (Email, position))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Orders_path = os.path.join('NittanyBusinessDataset_v3', 'Orders.csv')

    Ordersdata = pd.read_csv(Orders_path)

    for _, row in Ordersdata.iterrows():
        orderID = row['Order_ID']
        sellerEmail = row['Seller_Email']
        listingID = row['Listing_ID']
        buyerEmail = row['Buyer_Email']
        date = row['Date']
        qty = row['Quantity']
        payment = row['Payment']

        cursor.execute('''INSERT OR IGNORE INTO Orders (Order_ID, Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment) VALUES (?, ?, ?, ?, ?, ?, ?)''', (orderID, sellerEmail, listingID, buyerEmail, date, qty, payment))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    ProductListings_path = os.path.join('NittanyBusinessDataset_v3', 'Product_Listings.csv')

    ProductListingsdata = pd.read_csv(ProductListings_path)

    for _, row in ProductListingsdata.iterrows():
        sellerEmail = row['Seller_Email']
        listingID = row['Listing_ID']
        category = row['Category']
        producttitle = row['Product_Title']
        productName = row['Product_Name']
        productDesc = row['Product_Description']
        qty = row['Quantity']
        productPrice = row['Product_Price']
        status = row['Status']

        cursor.execute('''INSERT OR IGNORE INTO Product_Listings (Seller_Email, Listing_ID, Category, Product_Title, Product_Name, Product_Description, Quantity, Product_Price, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (sellerEmail, listingID, category, producttitle, productName, productDesc, qty, productPrice, status))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Requests_path = os.path.join('NittanyBusinessDataset_v3', 'Requests.csv')

    Requestsdata = pd.read_csv(Requests_path)

    for _, row in Requestsdata.iterrows():
        reqID = row['request_id']
        senderEmail = row['sender_email']
        helpdeskEmail = row['helpdesk_staff_email']
        reqtype = row['request_type']
        reqdesc = row['request_desc']
        reqstatus = row['request_status']

        cursor.execute('''INSERT OR IGNORE INTO Requests (request_id, sender_email, helpdesk_staff_email, request_type, request_desc, request_status) VALUES (?, ?, ?, ?, ?, ?)''', (reqID, senderEmail, helpdeskEmail, reqtype, reqdesc, reqstatus))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Reviews_path = os.path.join('NittanyBusinessDataset_v3', 'Reviews.csv')

    Reviewsdata = pd.read_csv(Reviews_path)

    for _, row in Reviewsdata.iterrows():
        orderID = row['Order_ID']
        rate = row['Rate']
        reviewdesc = row['Review_Desc']

        cursor.execute('''INSERT OR IGNORE INTO Reviews (Order_ID, Rate, Review_Desc) VALUES (?, ?, ?)''', (orderID, rate, reviewdesc))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Sellers_path = os.path.join('NittanyBusinessDataset_v3', 'Sellers.csv')

    Sellersdata = pd.read_csv(Sellers_path)

    for _, row in Sellersdata.iterrows():
        email = row['email']
        business_name = row['business_name']
        Business_Address_ID = row['Business_Address_ID']
        bank_routing_number = row['bank_routing_number']
        bank_account_number = row['bank_account_number']
        balance = row['balance']

        cursor.execute(
            '''INSERT OR IGNORE INTO Sellers (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, balance) VALUES (?, ?, ?, ?, ?, ?)''',
            (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, balance))

    connection.commit()
    connection.close()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    Zipcode_Info_path = os.path.join('NittanyBusinessDataset_v3', 'Zipcode_Info.csv')

    Zipcode_Info_data = pd.read_csv(Zipcode_Info_path)

    for _, row in Zipcode_Info_data.iterrows():
        zipcode = row['zipcode']
        city = row['city']
        state = row['state']

        cursor.execute('''INSERT OR IGNORE INTO Zipcode_Info (zipcode, city, state) VALUES (?, ?, ?)''',
                       ((zipcode, city, state)))

    connection.commit()
    connection.close()


def create_app():
    app = Flask(__name__)
    host = 'http://127.0.0.1:5000/'
    createDB()
    insertUsers()
    return app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html', loginFailed=False)

@app.route('/')
@app.route('/Login', methods=['POST', 'GET']) #PRESS LOG IN
def name():
    error = None
    if request.method == 'POST':
        hashedPw = hash(request.form['Password'])
        result = valid_login(request.form['Email'], hashedPw)
        if result:
            return render_template('landingPage.html', email=request.form['Email'])#go to landing page
        else:
            return render_template("index.html", loginFailed=True)
    else:
        return render_template("index.html", loginFailed=False)

@app.route('/CreateAccount', methods=['POST', 'GET']) #PRESS LOG IN
def input():
    if request.method == 'POST':
        if request.form['Password'] != request.form['confirmPassword']:
            return render_template('input.html', incorrectID = False, passwordsNotMatch=True, acctExist=False)
        else:#passwords match
            potentailUserID = request.form['Email']

            if "@" not in potentailUserID:
                print("Invalid User ID")
                return render_template('input.html', incorrectID=True, passwordsNotMatch=False, acctExist=False)

            hashedPw = hash(request.form['Password'])
            connection = sql.connect('database.db')
            email = request.form['Email']
            matches = connection.execute('SELECT COUNT(*) as rows FROM Users WHERE email = ?',(email,))  # get all users with email
            result = matches.fetchone()
            if result is not None and result[0] is not None and int(result[0]) > 0:
                return render_template('input.html', incorrectID = False, passwordsNotMatch=False, acctExist=True)
            else: #new entry
                connection.execute('INSERT INTO Users (email, password) VALUES (?,?);', (request.form["Email"], hashedPw))
                connection.commit()
                return render_template('landingPage.html', email=request.form['Email'])#go to landing page

    return render_template('input.html')


def valid_login(email, password):#returns user if there is one that matches hashed input
    connection = sql.connect('database.db')
    matches = connection.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, password)) #get all users with user-pw combo
    return matches.fetchone()

if __name__ == "__main__":
    createDB()
    insertUsers()
    app.run()