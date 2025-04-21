from flask import Blueprint, request, session, jsonify
import sqlite3
from datetime import datetime

order_bp = Blueprint("order", __name__)

def get_db():
    return sqlite3.connect("nittanybusiness.db")

@order_bp.route("/place_order", methods=["POST"])
def place_order():
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    seller_email = data["seller_email"]
    listing_id = data["listing_id"]
    order_quantity = int(data["quantity"])
    buyer_email = session["email"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT Quantity, Product_Price FROM Product_Listings 
        WHERE Seller_Email = ? AND Listing_ID = ? AND Status = 1
    """, (seller_email, listing_id))
    result = cur.fetchone()

    if not result:
        return jsonify({"error": "Product not found or inactive"}), 400

    available_qty, price = result
    if order_quantity > available_qty:
        return jsonify({"error": "Not enough quantity available"}), 400

    payment = order_quantity * price
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO Orders (Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (seller_email, listing_id, buyer_email, order_date, order_quantity, payment))

    new_qty = available_qty - order_quantity
    new_status = 2 if new_qty == 0 else 1

    cur.execute("""
        UPDATE Product_Listings 
        SET Quantity = ?, Status = ? 
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (new_qty, new_status, seller_email, listing_id))

    cur.execute("""
        UPDATE Sellers SET balance = balance + ? WHERE email = ?
    """, (payment, seller_email))

    conn.commit()
    conn.close()

    return jsonify({"message": "Order placed successfully!"})





from werkzeug.security import generate_password_hash
from flask import Blueprint, request, session, jsonify

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/update_profile", methods=["POST"])
def update_profile():
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    email = session["email"]

    password = data.get("password")
    business_name = data.get("business_name")
    address = data.get("address", {})
    zipcode = address.get("zipcode")
    street_num = address.get("street_num")
    street_name = address.get("street_name")

    conn = get_db()
    cur = conn.cursor()

    if password:
        password_hash = generate_password_hash(password)
        cur.execute("UPDATE Users SET password = ? WHERE email = ?", (password_hash, email))

    if business_name:
        cur.execute("UPDATE Buyer SET business_name = ? WHERE email = ?", (business_name, email))

    cur.execute("SELECT buyer_address_id FROM Buyer WHERE email = ?", (email,))
    row = cur.fetchone()
    if row and all([zipcode, street_num, street_name]):
        address_id = row[0]
        cur.execute("""
            UPDATE Address
            SET zipcode = ?, street_num = ?, street_name = ?
            WHERE address_ID = ?
        """, (zipcode, street_num, street_name, address_id))

    conn.commit()
    conn.close()
    return jsonify({"message": "Profile updated successfully!"})

