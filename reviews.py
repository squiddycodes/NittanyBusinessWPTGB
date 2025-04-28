from flask import Blueprint, render_template, request
import sqlite3 as sql

reviews_bp = Blueprint('reviews', __name__, template_folder='templates')

@reviews_bp.route("/MakeReview", methods=['POST', 'GET'])
def reviews():
    rating = request.form.get('rateNumber')
    review = request.form.get('reviewInput')
    order_id = request.form.get('listing_id')

    print(f"Rating: {rating}")
    print(f"Review: {review}")
    print(f"Order ID (listing_id): {order_id}")

    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Reviews (Order_ID, Rate, Review_Desc) VALUES (?, ?, ?)', (order_id, review, rating))
    connection.commit()

    return render_template('productcatalogue.html')