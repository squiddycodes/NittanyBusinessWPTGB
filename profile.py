from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3 as sql
from werkzeug.security import generate_password_hash

editprofile_bp = Blueprint("editprofile", __name__, template_folder="templates")


@editprofile_bp.route("/editprofile", methods=["GET", "POST"])
def edit_profile():
    if "email" not in session:
        return redirect(url_for("login"))  # Redirect if not logged in

    email = session["email"]

    if request.method == "POST":
        new_business_name = request.form["business_name"]
        new_street = request.form["street"]
        new_city = request.form["city"]
        new_state = request.form["state"]
        new_zipcode = request.form["zipcode"]
        new_password = request.form["password"]

        conn = sql.connect("database.db")
        cur = conn.cursor()

        if new_password:
            hashed_password = generate_password_hash(new_password)
            cur.execute("""
                UPDATE Users
                SET BusinessName = ?, Street = ?, City = ?, State = ?, Zipcode = ?, Password = ?
                WHERE Email = ?
            """, (new_business_name, new_street, new_city, new_state, new_zipcode, hashed_password, email))
        else:
            cur.execute("""
                UPDATE Users
                SET BusinessName = ?, Street = ?, City = ?, State = ?, Zipcode = ?
                WHERE Email = ?
            """, (new_business_name, new_street, new_city, new_state, new_zipcode, email))

        conn.commit()
        conn.close()

        return redirect(url_for("editprofile.edit_profile"))  # Refresh page

    # GET: Load current user data
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT BusinessName, Street, City, State, Zipcode FROM Users WHERE Email = ?", (email,))
    user_data = cur.fetchone()
    conn.close()

    return render_template("profile.html", email=email, user=user_data)

