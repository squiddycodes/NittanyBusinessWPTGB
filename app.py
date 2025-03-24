from flask import Flask, render_template, request, redirect, url_for #redirect used in routeToPage, for dropdown ease of access
import sqlite3 as sql
import hashlib

# Derek Guidorizzi, Joe Long, Nicole Chen, Bhavishya Malla
# We've Played these Games Before
# CMPSC 431W Section 1
# Nittany Business Phase 2 Demo

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('index.html', loginFailed=False)

@app.route('/')
@app.route('/Login', methods=['POST', 'GET']) #PRESS LOG IN
def name():
    error = None
    if request.method == 'POST':
        hashedPw = hash(request.form['Password'])
        result = valid_login(request.form['Email'], hashedPw)
        if result:
            return render_template('landingPage.html', email=request.form['Email'])#go to landing page
        else:
            return render_template("index.html", loginFailed=True)
    else:
        return render_template("index.html", loginFailed=False)

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
            print(email)
            matches = connection.execute('SELECT * FROM Users WHERE email = ?', (email,))  # get all users with email
            print(matches.fetchone())
            if matches.fetchone():
                print("account already exists")
                return render_template('input.html', incorrectID = False, passwordsNotMatch=False, acctExist=True)
            else: #new entry
                connection.execute('INSERT INTO Users (email, password) VALUES (?,?);', (request.form["Email"], hashedPw))
                connection.commit()
                return render_template('landingPage.html', email=request.form['Email'])#go to landing page

    return render_template('input.html')


def valid_login(email, password):#returns user if there is one that matches hashed input
    connection = sql.connect('database.db')
    matches = connection.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, password)) #get all users with user-pw combo
    return matches.fetchone()

def hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    app.run()


