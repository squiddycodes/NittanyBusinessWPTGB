from flask import Blueprint, request, session, jsonify, render_template
from datetime import datetime
import sqlite3 as sql

order_bp = Blueprint('order', __name__, template_folder='templates')


@order_bp.route("/place_order", methods=["POST"])
def place_order():
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    seller_email = request.form["Seller_Email"]
    listing_id = request.form["Listing_ID"]
    order_quantity = int(request.form["Quantity"])
    buyer_email = session["email"]

    # Connect to the database using sqlite3
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Quantity, Product_Price FROM Product_Listings 
        WHERE Seller_Email = ? AND Listing_ID = ? AND Status = 1
    """, (seller_email, listing_id))
    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "Product not found or inactive"}), 400

    available_qty, price = result
    if order_quantity > available_qty:
        return jsonify({"error": "Not enough quantity available"}), 400

    payment = order_quantity * price
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO Orders (Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (seller_email, listing_id, buyer_email, order_date, order_quantity, payment))

    new_qty = available_qty - order_quantity
    new_status = 2 if new_qty == 0 else 1

    cursor.execute("""
        UPDATE Product_Listings 
        SET Quantity = ?, Status = ? 
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (new_qty, new_status, seller_email, listing_id))

    cursor.execute("""
        UPDATE Sellers SET balance = balance + ? WHERE email = ?
    """, (payment, seller_email))

    connection.commit()
    connection.close()

    return jsonify({"message": "Order placed successfully!"})


@order_bp.route("/confirm_order", methods=["POST"])
def confirm_order():
    if "email" not in session:
        return "Unauthorized", 401

    seller_email = request.form['Seller_Email ']
    product_name = request.form['Product_name']
    quantity = int(request.form['Quantity'])
    unit_price = float(request.form['Product_Price'])

    # Connect to the database using sqlite3
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Product_Listings (Seller_Email, Product_Name, Quantity, Product_Price, Status)
        VALUES (?, ?, ?, ?, 1)
    """, (seller_email, product_name, quantity, unit_price))

    connection.commit()
    connection.close()

    return render_template("sellersLandingPage.html", email=seller_email)
