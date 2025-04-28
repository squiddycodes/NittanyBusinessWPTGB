from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 as sql
import random
import hashlib
from werkzeug.security import generate_password_hash

editBuyerprofile_bp = Blueprint("editBuyerprofile", __name__, template_folder="templates")

def hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

@editBuyerprofile_bp.route("/EditProfileInformationBuyers", methods=["GET", "POST"])
def edit_profile():

    email = request.form['email']

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Users WHERE email = ?", (email,))
    buyer_login = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT business_name, buyer_address_id FROM Buyers WHERE email = ?", (email,))
    buyer_data = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT zipcode, street_name, street_num FROM Address WHERE address_id = ?", (buyer_data[1],))
    buyer_address = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT city, state FROM Zipcode_Info WHERE zipcode = ?", (buyer_address[0],))
    buyer_location = cur.fetchone()
    conn.close()

    return render_template("buyereditprofile.html",
                           email=email,
                           buyer_login=buyer_login,
                           buyer_data = buyer_data,
                           buyer_address = buyer_address,
                           buyer_location = buyer_location)

@editBuyerprofile_bp.route("/UpdateBuyerProfile", methods=["GET", "POST"])
def updateBuyerProfile():
    email = request.form['email']

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Users WHERE email = ?", (email,))
    buyer_login = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT business_name, buyer_address_id FROM Buyers WHERE email = ?", (email,))
    buyer_data = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT zipcode, street_name, street_num FROM Address WHERE address_id = ?", (buyer_data[1],))
    buyer_address = cur.fetchone()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT city, state FROM Zipcode_Info WHERE zipcode = ?", (buyer_address[0],))
    buyer_location = cur.fetchone()
    conn.close()

    newUserID = request.form.get('newUserID', '').strip()
    if not newUserID:
        newUserID = email

    newPassword = request.form.get('newPassword', '').strip()
    if not newPassword:
        newPassword = buyer_login[0]
    else:
        newPassword = hash(newPassword)

    newBusinessName = request.form.get('newBusinessName')
    if not newBusinessName:
        newBusinessName = buyer_data[0]

    newStreetName = request.form.get('newStreetName')
    if not newStreetName:
        newStreetName = buyer_address[1]

    newStreetNum = request.form.get('newStreetNum', '').strip()
    if not newStreetNum:
        newStreetNum = buyer_address[2]

    newZipcode = request.form.get('newZipcode', '').strip()
    if not newZipcode:
        newZipcode = buyer_address[0]

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Zipcode_Info WHERE zipcode = ?", (newZipcode,))
    checkZipcode = cur.fetchone()
    conn.close()

    if checkZipcode[0] == 0:
        return render_template("buyereditprofile.html",
                           email=email,
                           buyer_login=buyer_login,
                           buyer_data = buyer_data,
                           buyer_address = buyer_address,
                           buyer_location = buyer_location,
                           invalidZipcode=True)

    oldPassword = request.form.get('verifyCurrPW')
    oldHashedPW = hash(oldPassword)

    if buyer_login[0] != oldHashedPW:
        return render_template("buyereditprofile.html",
                               email=email,
                               buyer_login=buyer_login,
                               buyer_data=buyer_data,
                               buyer_address=buyer_address,
                               buyer_location=buyer_location,
                               incorrectCurrPW=True)

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Users SET password = ? WHERE email = ?", (newPassword,email,))
    conn.commit()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Buyers SET business_name = ? WHERE email = ?", (newBusinessName,email,))
    conn.commit()
    conn.close()

    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE Address SET zipcode = ?, street_name = ?, street_num = ? WHERE address_id = ?", (newZipcode, newStreetName, newStreetNum, buyer_data[1],))
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


        cur.execute("INSERT INTO Requests (request_id, sender_email, helpdesk_staff_email, request_type, request_desc, request_status) VALUES (?,?,?,?,?,?)", (new_id, email, UserIDHelpDesk, 'ChangeID', NewIDRequest, '0',))
        conn.commit()
        conn.close()

    return render_template('buyersLandingPage.html', email=email)