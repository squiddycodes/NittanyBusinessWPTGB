from flask import Flask, Blueprint, render_template, request
import sqlite3 as sql
import hashlib
#from app import create_app

#app = create_app()
browseproducts_bp = Blueprint('browseproducts', __name__, template_folder='templates')

@browseproducts_bp.route('/BrowseProducts', methods=['POST', 'GET']) #PRESS LOG IN
def input():
    print("hello world")