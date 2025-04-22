from flask import Blueprint, render_template, request
import sqlite3 as sql
import hashlib
import os
import pandas as pd

#app = create_app()
registration_bp = Blueprint('registration', __name__, template_folder='templates')
# create account option on input page already--move the page that create account button
# redirects to onto this file :)
@registration_bp.route("/registration")

def hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

# Find if the address that the user inputs during creation is linked to an address ID
def getAddress(streetnum, streetname, zipcode):
    address_path = os.path.join('NittanyBusinessDataset_v3', 'Address.csv')
    address_data = pd.read_csv(address_path)

    for _, row in address_data.iterrows():
        dfStreetNum = row['street_number']
        dfStreetName = row['street_name'].strip().lower()   # in case of extra spaces/inputting lowercase address
        dfZipcode = str(row['zipcode'])

        if dfStreetNum == streetnum and dfStreetName == streetname.strip().lower() and dfZipcode == zipcode:
            return row['address_id']

    return None

@registration_bp.route('/CreateAccount', methods=['POST', 'GET']) #PRESS CREATE ACCOUNT
def input():
    email = request.form.get('Email')
    password = request.form.get('Password')
    confirm_pwd = request.form.get('confirmPassword')
    account_type = request.form.get('accountType')

    if request.method == 'POST':
        print("TESTING FOR NOW")    # Form not being submitted/attempted to submit at all
        if password != confirm_pwd:
            return render_template('input.html', incorrectID = False, passwordsNotMatch=True, acctExist=False)

        if "@" not in email:
            print("Invalid User ID")
            return render_template('input.html', incorrectID=True, passwordsNotMatch=False, acctExist=False)

        hashedPw = hash(password)
        connection = sql.connect('database.db')
        matches = connection.execute('SELECT COUNT(*) as rows FROM Users WHERE email = ?',(email,))  # get all users with email
        result = matches.fetchone()
        if result is not None and result[0] is not None and int(result[0]) > 0:
            return render_template('input.html', incorrectID = False, passwordsNotMatch=False, acctExist=True)
        else: #new entry
            connection.execute('INSERT INTO Users (email, password) VALUES (?,?);', (email, hashedPw))

            if account_type == 'buyer':
                business = request.form.get('buyerBusiness')
                street_num = request.form.get('buyerStNum')
                street_name = request.form.get('buyerStName')
                zip_code = request.form.get('buyerZip')

                address_id = getAddress(street_num, street_name, zip_code)
                if address_id is None:
                    print("Invalid address information")
                    connection.rollback()
                    return render_template('input.html', invalidAddress = True)

                connection.execute('INSERT INTO Buyers (email, business_name, buyer_address_id) VALUES (?,?,?)', (email, business, address_id))
                connection.commit()
                return render_template('buyersLandingPage.html', email=email)

            elif account_type == 'seller':
                business = request.form.get('sellerBusiness')
                street_num = request.form.get('sellerStNum')
                street_name = request.form.get('sellerStName')
                zip_code = request.form.get('sellerZip')
                routing_num = request.form.get('sellerRoutNum')
                account_num = request.form.get('sellerAccNum')

                address_id = getAddress(street_num, street_name, zip_code)
                if address_id is None:
                    print("Invalid address information")
                    connection.rollback()
                    return render_template('input.html', invalidAddress=True)

                connection.execute('INSERT INTO Sellers (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, balance)'
                                   'VALUES (?,?,?,?,?,?)', (email, business, address_id, routing_num, account_num,0))
                connection.commit()
                return render_template('sellersLandingPage.html', email=email)

            elif account_type == 'helpdesk':
                helpdesk_position = request.form.get('hdPosition')

                connection.execute('INSERT INTO Helpdesk (email, Position) VALUES (?,?)', (email, helpdesk_position))
                connection.commit()

                # go back to home (could show a message indicating account needs to be approved)
                return render_template('index.html', email=email)

    return render_template('input.html')

# more information drops down based on user type select (e.g. if select Buyer, enter
# certain info, seller, enter other info, etc.)

# if user selects to create a helpdesk account, needs approval from admin--admin approval task?
# mark as approved or not approved

# Seller: Bank balance should be 0 upon registration. Bank routing num should be 8 numbers, account num 6 numbers