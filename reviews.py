from flask import Blueprint, render_template, request, url_for, redirect
import sqlite3 as sql

reviews_bp = Blueprint('reviews', __name__, template_folder='templates')

@reviews_bp.route("/MakeReview", methods=['POST', 'GET'])
def reviews():
    rating = request.form.get('rateNumber')
    review = request.form.get('reviewInput')
    order = request.form.get('order_id')

    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Reviews (Order_ID, Rate, Review_Desc) VALUES (?, ?, ?)', (order, rating, review))
    connection.commit()

    return redirect(url_for('BrowseProducts.browse_products', currCategory="Root", email=request.form.get('email'), keyword="", keywordInput=""))