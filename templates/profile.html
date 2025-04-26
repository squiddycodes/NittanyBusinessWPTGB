from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3 as sql
from werkzeug.security import generate_password_hash

profile_bp = Blueprint("profile", __name__, template_folder="templates")


@profile_bp.route("/profile", methods=["GET", "POST"])
def update_profile():
    if "email" not in session:
        return redirect(url_for("login"))  # or your login route

    email = session["email"]

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        new_password = request.form["password"]

        conn = sql.connect("database.db")
        cur = conn.cursor()

        if new_password:
            hashed_password = generate_password_hash(new_password)
            cur.execute("""
                UPDATE Users
                SET Name = ?, Phone = ?, Address = ?, Password = ?
                WHERE Email = ?
            """, (name, phone, address, hashed_password, email))
        else:
            cur.execute("""
                UPDATE Users
                SET Name = ?, Phone = ?, Address = ?
                WHERE Email = ?
            """, (name, phone, address, email))

        conn.commit()
        conn.close()

        return redirect(url_for("profile.update_profile"))  # refresh the page

    # GET: Load user data
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT Name, Phone, Address FROM Users WHERE Email = ?", (email,))
    user_data = cur.fetchone()
    conn.close()

    return render_template("profile.html", email=email, user=user_data)

