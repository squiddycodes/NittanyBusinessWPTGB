from flask import Blueprint, render_template

reviews_bp = Blueprint('reviews', __name__, template_folder='templates')

@reviews_bp.route("/reviews")
def reviews():
    return 'Hello, World!'