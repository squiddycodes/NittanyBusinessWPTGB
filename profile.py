from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3 as sql
from werkzeug.security import generate_password_hash

editprofile_bp = Blueprint("editprofile", __name__, template_folder="templates")

@editprofile_bp.route("/EditProfileInformation", methods=["GET", "POST"])
def edit_profile():
    if request.method == "GET":
        email = request.args.get("email")
        if not email:
            return redirect(url_for("login"))  # Redirect if email not provided

        conn = sql.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT BusinessName, Street, City, State, Zipcode FROM Users WHERE Email = ?", (email,))
        user_data = cur.fetchone()
        conn.close()

        return render_template("profile.html", email=email, user=user_data)

    # POST request: user is submitting updated form
    email = request.form.get("email")
    if not email:
        return redirect(url_for("login"))

    new_business_name = request.form.get("business_name")
    new_street = request.form.get("street")
    new_city = request.form.get("city")
    new_state = request.form.get("state")
    new_zipcode = request.form.get("zipcode")
    new_password = request.form.get("password")

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

    # After editing profile, send back to the appropriate landing page
    return redirect(url_for("landing_page", email=email))

