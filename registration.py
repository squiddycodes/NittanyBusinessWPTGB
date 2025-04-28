from flask import Blueprint, render_template, request
import sqlite3 as sql
import hashlib
import os
import pandas as pd
import random

#app = create_app()
registration_bp = Blueprint('registration', __name__, template_folder='templates')
# create account option on input page already--move the page that create account button
# redirects to onto this file :)
@registration_bp.route("/registration")

def hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

# Find if the address that the user inputs during creation is linked to an address ID
def getAddress(zipcode, streetnum, streetname, connection):
    address_path = os.path.join('NittanyBusinessDataset_v3', 'Address.csv')
    address_data = pd.read_csv(address_path)

    fullAddr = address_data[
        # Input type in html form is text, convert database info to string
        (address_data["zipcode"].astype(str) == zipcode) &
        (address_data["street_num"].astype(str) == streetnum) &
        (address_data["street_name"].astype(str) == streetname)
    ]

    # No matching address found in database, add to database and create new address ID
    if fullAddr.empty:
        existing_ids = set(address_data['address_id'].astype(str))

        # Continue generating IDs until a unique one is made
        while True:
            newId = ''.join(random.choices('0123456789abcdef', k=32))
            if newId not in existing_ids:
                break

        cursor = connection.cursor()
        cursor.execute("INSERT INTO Address (address_id, zipcode, street_num, street_name) VALUES (?,?,?,?)", (newId, zipcode, streetnum, streetname))
        connection.commit()

        return newId

    return fullAddr.iloc[0]["address_id"]

@registration_bp.route('/CreateAccount', methods=['POST', 'GET']) #PRESS CREATE ACCOUNT
def input():
    # connection = sql.connect('database.db')
    # cursor = connection.cursor()
    # cursor.execute("SELECT position FROM Helpdesk WHERE email = ?", ("request.form['Email']",))
    # result = cursor.fetchone()

    email = request.form.get('Email')
    password = request.form.get('Password')
    confirm_pwd = request.form.get('confirmPassword')
    account_type = request.form.get('accountType')

    if request.method == 'POST':
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

                address_id = getAddress(zip_code, street_num, street_name, connection)
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

                address_id = getAddress(zip_code, street_num, street_name, connection)
                if address_id is None:
                    print("Invalid address information")
                    connection.rollback()
                    return render_template('input.html', invalidAddress=True)

                connection.execute('INSERT INTO Sellers (email, business_name, Business_Address_ID, bank_routing_number, bank_account_number, balance)'
                                   'VALUES (?,?,?,?,?,?)', (email, business, address_id, routing_num, account_num, 0))

                connection.commit()
                return render_template('sellersLandingPage.html', email=email)

            elif account_type == 'helpdesk':
                helpdesk_position = request.form.get('helpPosition')
                UserIDHelpDesk = 'u0fvl3dj@nittybiz.com'
                NewIDRequest = "Please create my helpdesk staff account - position:" + helpdesk_position
                new_id = random.randint(1, 600)
                unique = False

                cur = connection.cursor()
                while not unique:
                    matching_listid = cur.execute('SELECT COUNT(*) as rows FROM Requests WHERE request_id = ?',
                                                  (new_id,))

                    if matching_listid.fetchone()[0] <= 0:
                        unique = True
                    else:
                        new_id = random.randint(1, 600)


                connection.execute('INSERT INTO Helpdesk (email, Position) VALUES (?,?)', (email, helpdesk_position+' - Not Approved'))
                cur.execute("INSERT INTO Requests (request_id, sender_email, helpdesk_staff_email, request_type, request_desc, request_status) VALUES (?,?,?,?,?,?)", (new_id, email, UserIDHelpDesk, 'HelpDeskRegistration', NewIDRequest, '0',))
                connection.commit()

                return render_template('input.html', email=email, requestApproval=True)

    return render_template('input.html')

# if user selects to create a helpdesk account, needs approval from admin--admin approval task?
# mark as approved or not approved