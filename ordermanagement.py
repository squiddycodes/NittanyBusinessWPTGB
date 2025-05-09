from flask import Blueprint, request, render_template, url_for, redirect
import sqlite3 as sql
import random
from datetime import datetime
import os
import pandas as pd
order_bp = Blueprint("order", __name__, template_folder='templates')

@order_bp.route("/place_order", methods=["POST"])
def place_order():
    # Extract buyer and seller information from the form
    buyer_email = request.form['email']
    seller_email = request.form['seller_email']
    listing_id = request.form['listing_id']
    order_quantity = int(request.form['QtyToBuy'])  # The quantity the buyer wants to purchase

    # Connect to the database
    conn = sql.connect('database.db')
    cur = conn.cursor()

    # Fetch product information based on the seller's email and listing ID
    cur.execute("""
        SELECT Seller_Email, Product_Title, Product_Name, Product_Description, Category, Product_Price, Quantity
        FROM Product_Listings
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (seller_email, listing_id))
    product_data = cur.fetchone()

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT AVG(Rate) AS seller_rating FROM Reviews WHERE Order_ID IN (SELECT Order_ID From Orders WHERE Seller_Email = ?)',
        (seller_email,))
    seller_rating = cursor.fetchone()
    connection.close()



    # If the product is not found, return an error message
    if not product_data:
        conn.close()
        return "Product not found."

    seller_email, product_title, product_name, product_description, product_category, unit_price, available_qty = product_data

    # Check if the requested quantity is available
    if order_quantity > available_qty:
        return render_template('productpage.html', email=buyer_email, product=product_data, listing_id = listing_id, seller_rating=seller_rating, overQty=True)
        #return redirect(url_for('BrowseProducts.browse_product', listing_id=listing_id,email=buyer_email))


    # Clean the unit_price by removing the dollar sign and converting it to a float
    unit_price = int(unit_price.replace('$', '').strip())

    # Calculate the payment (total cost) based on  quantity and unit price
    payment = unit_price * order_quantity

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT AVG(Rate) AS seller_rating FROM Reviews WHERE Order_ID IN (SELECT Order_ID From Orders WHERE Seller_Email = ?)',
        (seller_email,))
    seller_rating = cursor.fetchone()
    connection.close()

    # Render the order confirmation page with the necessary details
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
                            available_qty=available_qty,
                            seller_rating=seller_rating)


@order_bp.route("/confirm_order", methods=["POST"])
def confirm_order():
    # Extract order details from the form
    buyer_email = request.form['buyer_email']
    seller_email = request.form['seller_email']
    listing_id = request.form['listing_id']
    quantity_ordered = int(request.form['quantity'])
    payment = float(request.form['payment'])
    # Get the current date and time for the order
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Connect to the database
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
    if new_quantity == 0:
        # If stock is now 0, set Status = 2
        cur.execute("""
            UPDATE Product_Listings
            SET Quantity = ?, Status = 2
            WHERE Seller_Email = ? AND Listing_ID = ?
        """, (new_quantity, seller_email, listing_id))
    else:
        # Otherwise, just update Quantity
        cur.execute("""
            UPDATE Product_Listings
            SET Quantity = ?
            WHERE Seller_Email = ? AND Listing_ID = ?
        """, (new_quantity, seller_email, listing_id))
    conn.commit()

    # Insert the order into the Orders table
    review_path = os.path.join('NittanyBusinessDataset_v3', 'Reviews.csv')
    review_data = pd.read_csv(review_path)
    existing_orders = set(review_data['Order_ID'])
    while True:
        order_id = random.randint(1, 9999)
        if order_id not in existing_orders:
            break

    cur.execute("""
        INSERT INTO Orders (Order_ID, Seller_Email, Listing_ID, Buyer_Email, Date, Quantity, Payment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_id, seller_email, listing_id, buyer_email, order_date, quantity_ordered, payment))

    # Commit the transaction
    conn.commit()

    # Fetch updated product info
    cur.execute("""
        SELECT Product_Title, Product_Name, Product_Description, Category, Product_Price, Quantity
        FROM Product_Listings
        WHERE Seller_Email = ? AND Listing_ID = ?
    """, (seller_email, listing_id))
    updated_product = cur.fetchone()
    conn.close()

    if not updated_product:
        return "Error fetching updated product."

    product_title, product_name, product_description, product_category, unit_price, available_qty = updated_product
    unit_price = unit_price.replace("$","")
    product = [
        seller_email,
        product_title,
        product_name,
        product_description,
        product_category,
        unit_price,
        available_qty
    ]

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT AVG(Rate) AS seller_rating FROM Reviews WHERE Order_ID IN (SELECT Order_ID From Orders WHERE Seller_Email = ?)',
        (product[0],))
    seller_rating = cursor.fetchone()

    connection.close()

    return render_template("orderconfirmation.html",
                           buyer_email=buyer_email,
                           seller_email=seller_email,
                           listing_id=listing_id,
                           quantity=quantity_ordered,
                           payment=payment,
                           product_title=product_title,
                           product_name=product_name,
                           product_description=product_description,
                           product_category=product_category,
                           unit_price=unit_price,
                           available_qty=available_qty,
                           seller_rating=seller_rating,
                           order_id = order_id,
                           orderSubmitted=True)
