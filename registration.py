from flask import Flask, Blueprint, render_template, request
import sqlite3 as sql
from app import hash
from app import create_app

app = create_app()
registration_bp = Blueprint('registration', __name__, template_folder='templates')
# create account option on input page already--move the page that create account button
# redirects to onto this file :)
@registration_bp.route("/registration")

@app.route('/CreateAccount', methods=['POST', 'GET']) #PRESS LOG IN
def input():
    if request.method == 'POST':
        if request.form['Password'] != request.form['confirmPassword']:
            return render_template('input.html', incorrectID = False, passwordsNotMatch=True, acctExist=False)
        else:#passwords match
            potentailUserID = request.form['Email']

            if "@" not in potentailUserID:
                print("Invalid User ID")
                return render_template('input.html', incorrectID=True, passwordsNotMatch=False, acctExist=False)

            hashedPw = hash(request.form['Password'])
            connection = sql.connect('database.db')
            email = request.form['Email']
            matches = connection.execute('SELECT COUNT(*) as rows FROM Users WHERE email = ?',(email,))  # get all users with email
            result = matches.fetchone()
            if result is not None and result[0] is not None and int(result[0]) > 0:
                return render_template('input.html', incorrectID = False, passwordsNotMatch=False, acctExist=True)
            else: #new entry
                connection.execute('INSERT INTO Users (email, password) VALUES (?,?);', (request.form["Email"], hashedPw))
                connection.commit()
                return render_template('landingPage.html', email=request.form['Email'])#go to landing page

    return render_template('input.html')

# more information drops down based on user type select (e.g. if select Buyer, enter
# certain info, seller, enter other info, etc.)

# if user selects to create a helpdesk account, needs approval from admin--admin approval task?
# mark as approved or not approved