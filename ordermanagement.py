from flask import Blueprint, request, render_template
import sqlite3 as sql
from datetime import datetime

order_bp = Blueprint("order", __name__, template_folder='templates')

@order_bp.route("/place_order", methods=["POST"])
def place_order():
    buyer_email = request.form['email']       # Buyer's email passed from form
    seller_email = request.form['seller_email']
    listing_id = request.form['listing_id']
    order_quantity = int(request.form['QtyToBuy'])  # How much the buyer wants to buy

    conn = sql.connect('database.db')
    cur = conn.cursor()

    # Fetch product info
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

    # Check if requested quantity is available
    if order_quantity > available_qty:
        return "Requested quantity exceeds available stock."

    payment = unit_price * order_quantity

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
                            available_qty=available_qty
                            )


@order_bp.route("/confirm_order", methods=["POST"])
def confirm_order():
    buyer_email = request.form['buyer_email']
    seller_email = request.form['seller_email']
    listing_id = request.form['listing_id']
    quantity_ordered = int(request.form['quantity'])

    conn = sql.connect('database.db')
    cur = conn.cursor()

    # First, get current available quantity
    cur.execute("""
        SELECT Quantity FROM Product_Listings
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (seller_email, listing_id))
    result = cur.fetchone()

    if not result:
        conn.close()
        return "Product not found."

    current_quantity = result[0]

    if quantity_ordered > current_quantity:
        conn.close()
        return "Not enough stock available."

    # Update quantity
    new_quantity = current_quantity - quantity_ordered
    cur.execute("""
        UPDATE Product_Listings
        SET Quantity = ?
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (new_quantity, seller_email, listing_id))
    conn.commit()

    # Fetch updated product info
    cur.execute("""
        SELECT Product_Title, Product_Name, Product_Description, Product_Category, Product_Price, Quantity
        FROM Product_Listings
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (seller_email, listing_id))
    updated_product = cur.fetchone()
    conn.close()

    if not updated_product:
        return "Error fetching updated product."

    product_title, product_name, product_description, product_category, unit_price, available_qty = updated_product

    product = [
        seller_email,
        product_title,
        product_name,
        product_description,
        product_category,
        unit_price,
        available_qty
    ]

    return render_template("productpage.html", email=buyer_email, product=product, listing_id=listing_id)

    







