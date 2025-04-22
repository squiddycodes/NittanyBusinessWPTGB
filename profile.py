from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash
from db import get_db  # import get_db from db.py

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/update_profile", methods=["POST"])
def update_profile():
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    email = session["email"]

    password = data.get("password")
    business_name = data.get("business_name")
    address = data.get("address", {})
    zipcode = address.get("zipcode")
    street_num = address.get("street_num")
    street_name = address.get("street_name")

    conn = get_db()
    cur = conn.cursor()

    if password:
        password_hash = generate_password_hash(password)
        cur.execute("UPDATE Users SET password = ? WHERE email = ?", (password_hash, email))

    if business_name:
        cur.execute("UPDATE Buyer SET business_name = ? WHERE email = ?", (business_name, email))

    cur.execute("SELECT buyer_address_id FROM Buyer WHERE email = ?", (email,))
    row = cur.fetchone()
    if row and all([zipcode, street_num, street_name]):
        address_id = row[0]
        cur.execute("""
            UPDATE Address
            SET zipcode = ?, street_num = ?, street_name = ?
            WHERE address_ID = ?
        """, (zipcode, street_num, street_name, address_id))

    conn.commit()
    conn.close()
    return jsonify({"message": "Profile updated successfully!"})
