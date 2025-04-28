from flask import Blueprint, render_template, request, url_for, redirect
import sqlite3 as sql
import random
import os
import pandas as pd

reviews_bp = Blueprint('reviews', __name__, template_folder='templates')

@reviews_bp.route("/MakeReview", methods=['POST', 'GET'])
def reviews():
    rating = request.form.get('rateNumber')
    review = request.form.get('reviewInput')

    review_path = os.path.join('NittanyBusinessDataset_v3', 'Reviews.csv')
    review_data = pd.read_csv(review_path)
    existing_orders = set(review_data['Order_ID'])
    while True:
        order_id = random.randint(1, 9999)
        if order_id not in existing_orders:
            break

    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Reviews (Order_ID, Rate, Review_Desc) VALUES (?, ?, ?)', (order_id, rating, review))
    connection.commit()

    return redirect(url_for('BrowseProducts.browse_products', currCategory="Root", email=request.form.get('email'), keyword="", keywordInput=""))