from flask import Flask, render_template, Blueprint

products_bp = Blueprint('products', __name__, template_folder='templates')