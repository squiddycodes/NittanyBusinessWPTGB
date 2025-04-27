from flask import Blueprint, render_template

reviews_bp = Blueprint('reviews', __name__, template_folder='templates')

@reviews_bp.route("/MakeReview", methods=['POST', 'GET'])
def reviews():
    return render_template('input.html', orderSubmitted=True)