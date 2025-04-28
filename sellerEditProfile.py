from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 as sql
import hashlib
import random
from werkzeug.security import generate_password_hash

editSellerprofile_bp = Blueprint("editSellerprofile", __name__, template_folder="templates")

def hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()
@editSellerprofile_bp.route("/EditSellerProfileInformation", methods=["GET", "POST"])
def edit_profile():

    email = request.form['email']

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Users WHERE email = ?", (email,))
    sellerPw = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT Business_Address_ID, business_name, bank_routing_number, bank_account_number FROM Sellers WHERE email = ?", (email,))
    seller_data = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT zipcode, street_name, street_num FROM Address WHERE address_id = ?", (seller_data[0],))
    seller_address = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT city, state FROM Zipcode_Info WHERE zipcode = ?", (seller_address[0],))
    seller_location = cur.fetchone()
    conn.close()

    return render_template("sellerEditProfile.html",
                           email=email,
                           sellerPw=sellerPw,
                           seller_data = seller_data,
                           seller_address = seller_address,
                           seller_location = seller_location)

@editSellerprofile_bp.route("/UpdateSellerProfile", methods=["GET", "POST"])
def updateSellerrProfile():
    email = request.form['email']

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Users WHERE email = ?", (email,))
    seller_login = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT Business_Address_ID, business_name, bank_routing_number, bank_account_number FROM Sellers WHERE email = ?", (email,))
    seller_data = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT zipcode, street_name, street_num FROM Address WHERE address_id = ?", (seller_data[0],))
    seller_address = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT city, state FROM Zipcode_Info WHERE zipcode = ?", (seller_address[0],))
    seller_location = cur.fetchone()
    conn.close()

    newUserID = request.form.get('newUserID', '').strip()
    if not newUserID:
        newUserID = email

    newPassword = request.form.get('newPassword', '').strip()
    if not newPassword:
        newPassword = seller_login[0]
    else:
        newPassword = hash(newPassword)

    newBusinessName = request.form.get('newBusinessName')
    if not newBusinessName:
        newBusinessName = seller_data[1]

    newRtingNum = request.form.get('oldRtingNum')
    if not newRtingNum:
        newRtingNum = seller_data[2]

    newAcctNum = request.form.get('oldAcctNum')
    if not newAcctNum:
        newAcctNum = seller_data[3]

    newStreetName = request.form.get('newStreetName')
    if not newStreetName:
        newStreetName = seller_address[1]

    newStreetNum = request.form.get('newStreetNum', '').strip()
    if not newStreetNum:
        newStreetNum = seller_address[2]

    newZipcode = request.form.get('newZipcode', '').strip()
    if not newZipcode:
        newZipcode = seller_address[0]

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Zipcode_Info WHERE zipcode = ?", (newZipcode,))
    checkZipcode = cur.fetchone()
    conn.close()

    if checkZipcode[0] == 0:
        return render_template("sellerEditProfile.html",
                               email=email,
                               sellerPw=seller_login,
                               seller_data=seller_data,
                               seller_address=seller_address,
                               seller_location=seller_location,
                               invalidZipcode=True)

    oldPassword = request.form.get('verifyCurrPW')
    oldHashedPW = hash(oldPassword)

    if seller_login[0] != oldHashedPW:
        return render_template("sellerEditProfile.html",
                               email=email,
                               sellerPw=seller_login,
                               seller_data=seller_data,
                               seller_address=seller_address,
                               seller_location=seller_location,
                               incorrectCurrPW=True)

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Users SET password = ? WHERE email = ?", (newPassword, email,))
    conn.commit()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Sellers SET business_name = ?, bank_routing_number = ?, bank_account_number = ? WHERE email = ?", (newBusinessName, newRtingNum, newAcctNum, email,))
    conn.commit()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Address SET zipcode = ?, street_name = ?, street_num = ? WHERE address_id = ?",
                (newZipcode, newStreetName, newStreetNum, seller_data[0],))
    conn.commit()
    conn.close()
    if newUserID != email:
        UserIDHelpDesk = 'u0fvl3dj@nittybiz.com'
        NewIDRequest = "Please change my name to " + newUserID
        new_id = random.randint(1, 600)
        unique = False

        conn = sql.connect("database.db")
        cur = conn.cursor()
        while not unique:
            matching_listid = cur.execute('SELECT COUNT(*) as rows FROM Requests WHERE request_id = ?', (new_id,))

            if matching_listid.fetchone()[0] <= 0:
                unique = True
            else:
                new_id = random.randint(1, 600)

        cur.execute(
            "INSERT INTO Requests (request_id, sender_email, helpdesk_staff_email, request_type, request_desc, request_status) VALUES (?,?,?,?,?,?)",
            (new_id, email, UserIDHelpDesk, 'ChangeID', NewIDRequest, '0',))
        conn.commit()
        conn.close()

    return render_template('sellersLandingPage.html', email=email)

@editSellerprofile_bp.route('/SellersHomePage', methods=['POST', 'GET'])
def returntoHomePage():
    email = ""
    if request.method == 'GET':
        email = request.args.get('email')
    elif request.method == 'POST':
        email = request.form['email']

    return render_template('sellersLandingPage.html', email = email)