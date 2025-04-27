from flask import Blueprint, request, render_template
import sqlite3 as sql
from datetime import datetime

order_bp = Blueprint("order", __name__, template_folder='templates')

@order_bp.route("/place_order", methods=["POST"])
def place_order():
    buyer_email = request.form['email']
    seller_email = request.form['seller_email']
    listing_id = request.form['listing_id']
    order_quantity = int(request.form['QtyToBuy'])

    conn = sql.connect('database.db')
    cur = conn.cursor()

    # Fetch product details
    cur.execute("""
        SELECT Product_Title, Product_Name, Product_Description, Product_Category, Product_Price, Quantity
        FROM Product_Listings 
        WHERE Seller_Email = ? AND Listing_ID = ? AND Status = 1
    """, (seller_email, listing_id))
    result = cur.fetchone()

    if not result:
        conn.close()
        return "Product not found or inactive."

    product_title, product_name, product_description, product_category, unit_price, available_qty = result

    if order_quantity > available_qty:
        conn.close()
        return "Not enough quantity available. Please go back and try again."

    payment = order_quantity * unit_price
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert into Orders table
    cur.execute("""
        INSERT INTO Orders (Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (seller_email, listing_id, buyer_email, order_date, order_quantity, payment))

    # Update Product_Listings
    new_qty = available_qty - order_quantity
    new_status = 2 if new_qty == 0 else 1

    cur.execute("""
        UPDATE Product_Listings 
        SET Quantity = ?, Status = ? 
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (new_qty, new_status, seller_email, listing_id))

    # Update Seller balance
    cur.execute("""
        UPDATE Sellers 
        SET balance = balance + ? 
        WHERE email = ?
    """, (payment, seller_email))

    conn.commit()
    conn.close()

    # Pass all needed data to the order confirmation page
    return render_template("orderconfirmation.html", 
                            buyer_email=buyer_email,
                            seller_email=seller_email,
                            listing_id=listing_id,
                            quantity=order_quantity,
                            payment=payment,
                            product_title=product_title,
                            product_name=product_name,
                            product_description=product_description,
                            product_category=product_category,
                            unit_price=unit_price,
                            available_qty=new_qty)  # updated quantity

@order_bp.route("/confirm_order", methods=["POST"])
def confirm_order():
    buyer_email = request.form['buyer_email']
    seller_email = request.form['seller_email']
    listing_id = request.form['listing_id']

    conn = sql.connect('database.db')
    cur = conn.cursor()

    # Fetch the latest product info
    cur.execute("""
        SELECT Product_Title, Product_Name, Product_Description, Product_Category, Product_Price, Quantity
        FROM Product_Listings
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (seller_email, listing_id))
    product_data = cur.fetchone()
    conn.close()

    if not product_data:
        return "Product not found."

    product_title, product_name, product_description, product_category, unit_price, available_qty = product_data

    product = [
        seller_email,
        product_title,
        product_name,
        product_description,
        product_category,
        unit_price,
        available_qty
    ]

    # Redirect buyer back to product page after confirming
    return render_template("productpage.html", email=buyer_email, product=product)







