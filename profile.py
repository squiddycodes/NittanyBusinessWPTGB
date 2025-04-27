from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql

# Define the Blueprint for profile-related routes
profile_bp = Blueprint('profile_bp', __name__, template_folder="templates"))

# Route to view the profile page
@profile_bp.route('/profile', methods=['GET'])
def view_profile():
    email = request.args.get('email')  # Get the email of the logged-in user

    # Fetch the current user's details from the database
    current_user = get_user_details(email)
    
    return render_template('profile.html', current_user=current_user)

# Route to edit the profile (this will allow users to edit their profile information)
@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    email = request.args.get('email')  # Get the email of the logged-in user

    # Fetch the current user's details from the database
    current_user = get_user_details(email)

    if request.method == 'POST':
        # Get the updated data from the form (excluding email)
        updated_name = request.form['name']
        updated_address = request.form['address']
        updated_phone = request.form['phone']
        updated_password = request.form['password']

        # If a password is entered, hash it before storing
        if updated_password:
            updated_password = generate_password_hash(updated_password)

        # Update the user's information in the database
        update_user_profile(email, updated_name, updated_address, updated_phone, updated_password)

        # Redirect to the profile page after successful update
        return redirect(url_for('profile_bp.view_profile', email=email))

    return render_template('editprofile.html', current_user=current_user)

# Function to get the current user's details
def get_user_details(email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name, address, phone, password FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()
    connection.close()

    if user:
        return {"email": email, "name": user[0], "address": user[1], "phone": user[2], "password": user[3]}
    else:
        return None

# Function to update the user's profile
def update_user_profile(email, name, address, phone, password=None):
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    if password:
        cursor.execute("""
            UPDATE Users
            SET name = ?, address = ?, phone = ?, password = ?
            WHERE email = ?
        """, (name, address, phone, password, email))
    else:
        cursor.execute("""
            UPDATE Users
            SET name = ?, address = ?, phone = ?
            WHERE email = ?
        """, (name, address, phone, email))

    connection.commit()
    connection.close()
