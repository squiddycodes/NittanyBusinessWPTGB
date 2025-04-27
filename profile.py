from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 as sql

# Define the Blueprint for profile-related routes
profile_bp = Blueprint('profile_bp', __name__, template_folder="templates"))

# Route to view the profile (this will show different pages based on user type)
@profile_bp.route('/profile')
def view_profile():
    email = request.args.get('email')  # Get the email of the logged-in user

    # Check user type to render the appropriate profile page
    user_type = get_user_type(email)
    
    if user_type == 'B':
        return render_template('buyersLandingPage.html', email=email)
    elif user_type == 'S':
        return render_template('sellersLandingPage.html', email=email)
    elif user_type == 'H':
        return render_template('helpdeskLandingPage.html', email=email)
    else:
        return redirect(url_for('index'))

# Route to edit the profile (this will allow users to edit their profile information)
@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    email = request.args.get('email')  # Get the email of the logged-in user

    if request.method == 'POST':
        # Get the updated data from the form
        updated_name = request.form['name']
        updated_address = request.form['address']
        updated_phone = request.form['phone']

        # Update the user's information in the database
        update_user_profile(email, updated_name, updated_address, updated_phone)

        # Redirect to the profile page after successful update
        return redirect(url_for('profile_bp.view_profile', email=email))

    return render_template('editproduct.html', email=email)

# Function to get the user type (Buyer, Seller, Helpdesk)
def get_user_type(email):
    result = ''
    connection = sql.connect('database.db')
    buyer = connection.execute('SELECT * FROM Buyers WHERE email = ?', (email,))
    seller = connection.execute('SELECT * FROM Sellers WHERE email = ?', (email,))
    helpdesk = connection.execute('SELECT * FROM HelpDesk WHERE email = ?', (email,))
    if buyer.fetchone():
        result += 'B'
    if seller.fetchone():
        result += 'S'
    if helpdesk.fetchone():
        result += 'H'
    return result

# Function to update the user's profile in the database
def update_user_profile(email, name, address, phone):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    
    cursor.execute('''UPDATE Users SET name = ?, address = ?, phone = ? WHERE email = ?''', 
                   (name, address, phone, email))
    
    connection.commit()
    connection.close()


