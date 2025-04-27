from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 as sql
from werkzeug.security import generate_password_hash

editprofile_bp = Blueprint("editprofile", __name__, template_folder="templates")


@editprofile_bp.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    # GET request: retrieve user info by email from query params
    if request.method == 'GET':
        email = request.args.get('email')
        if not email:
            return redirect(url_for('login'))
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT BusinessName, Street, City, State, Zipcode, Email FROM Users WHERE Email=?",
            (email,)
        )
        row = cursor.fetchone()
        conn.close()
        user = None
        if row:
            user = {
                'BusinessName': row[0],
                'Street': row[1],
                'City': row[2],
                'State': row[3],
                'Zipcode': row[4],
                'Email': row[5]
            }
        return render_template('profile.html', email=email, user=user)

    # POST request: update user info from form data
    email = request.form.get('email')
    if not email:
        return redirect(url_for('login'))
    businessName = request.form.get('BusinessName')
    street = request.form.get('Street')
    city = request.form.get('City')
    state = request.form.get('State')
    zipcode = request.form.get('Zipcode')
    password = request.form.get('Password')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if password:
        # Hash the new password before storing
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "UPDATE Users SET BusinessName=?, Street=?, City=?, State=?, Zipcode=?, Password=? WHERE Email=?",
            (businessName, street, city, state, zipcode, hashed_password, email)
        )
    else:
        cursor.execute(
            "UPDATE Users SET BusinessName=?, Street=?, City=?, State=?, Zipcode=? WHERE Email=?",
            (businessName, street, city, state, zipcode, email)
        )
    conn.commit()
    conn.close()

    # Reload the profile page after update
    return redirect(url_for('editprofile', email=email))
