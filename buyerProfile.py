from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 as sql
from werkzeug.security import generate_password_hash

editBuyerprofile_bp = Blueprint("editBuyerprofile", __name__, template_folder="templates")


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
    print("Hi")
