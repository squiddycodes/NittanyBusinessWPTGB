from flask import Blueprint, request, session, jsonify, render_template
import sqlite3 as sql
from datetime import datetime
#from db import get_db  # import get_db from db.py

order_bp = Blueprint("order", __name__)

@order_bp.route("/place_order", methods=["POST"])
def place_order():
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    seller_email = data["seller_email"]
    listing_id = data["listing_id"]
    order_quantity = int(data["quantity"])
    buyer_email = session["email"]

    conn = sql.connect('database.db')
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


@order_bp.route("/confirm_order", methods=["POST"])
def confirm_order():
    if "email" not in session:
        return "Unauthorized", 401

    seller_email = request.form['seller_email']
    product_name = request.form['product_name']
    quantity = int(request.form['quantity'])
    unit_price = float(request.form['unit_price'])

    conn = sql.connect('database.db')
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Product_Listings (Seller_Email, Product_Name, Quantity, Product_Price, Status)
        VALUES (?, ?, ?, ?, 1)
    """, (seller_email, product_name, quantity, unit_price))

    conn.commit()
    conn.close()

    return render_template("sellersLandingPage.html", email=seller_email)

