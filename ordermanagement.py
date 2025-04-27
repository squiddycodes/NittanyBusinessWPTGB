from flask import Blueprint, request, render_template
import sqlite3 as sql
from datetime import datetime

order_bp = Blueprint("order", __name__, template_folder='templates')

@order_bp.route("/place_order", methods=["POST"])
def place_order():
    # This was originally confirm_order functionality
    seller_email = request.form['seller_email']
    product_title = request.form['product_title']
    product_name = request.form['product_name']
    product_description = request.form['product_description']
    product_category = request.form['product_category']
    quantity = int(request.form['quantity'])
    unit_price = float(request.form['unit_price'])

    product = [
        seller_email,
        product_title,
        product_name,
        product_description,
        product_category,
        unit_price,
        quantity
    ]


return render_template("orderconfirmation.html", 
                           buyer_email=buyer_email,
                           seller_email=seller_email,
                           listing_id=listing_id,
                           quantity=order_quantity,
                           payment=payment)


@order_bp.route("/confirm_order", methods=["POST"])
def confirm_order():
    buyer_email = request.form['email']        # From hidden input
    seller_email = request.form['seller_email'] # From hidden input
    listing_id = request.form['listing_id']     # From hidden input
    quantity = int(request.form['QtyToBuy'])    # From hidden input

    conn = sql.connect('database.db')
    cur = conn.cursor()

    # Fetch the updated product info (after order placement)
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

    # Return the product page with updated info
    return render_template("productpage.html", email=buyer_email, product=product)


    







