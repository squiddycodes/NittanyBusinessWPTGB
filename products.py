from flask import Blueprint, render_template

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/MyProducts', methods=['POST', 'GET'])
def loadSellerProducts():
    return render_template('sellerproducts.html')

@products_bp.route('/ProductRegistration', methods=['POST', 'GET'])
def loadProductRegistrar():
    return render_template('productregisterform.html')