from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 as sql
from werkzeug.security import generate_password_hash

editSellerprofile_bp = Blueprint("editSellerprofile", __name__, template_folder="templates")


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
def updateBuyerProfile():
    print("Hi")

@editSellerprofile_bp.route('/SellersHomePage', methods=['POST', 'GET'])
def returntoHomePage():
    email = ""
    if request.method == 'GET':
        email = request.args.get('email')
    elif request.method == 'POST':
        email = request.form['email']

    return render_template('sellersLandingPage.html', email = email)