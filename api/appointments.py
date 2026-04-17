from flask import request, jsonify
from . import bp  # import the Blueprint instance
import sqlite3


@bp.route("/get_appointments", methods=["POST"])
async def get_appointments():
    data = request.json  # Get JSON data from frontend
    email_hash = data.get("email_hash")
    if not email_hash:
        return jsonify({"error": "Email is required"}), 400
    if not isinstance(email_hash, str):
        return jsonify({"error": "Invalid data type"}), 400
    
    with sqlite3.connect("db/CarEase.db") as conn:
        cursor = conn.cursor()
        try:
            # Fetch appointments for the given email join with services using service_id in appointments table
            cursor.execute("""
                SELECT a.*, s.*, t.* FROM appointments a
                JOIN services s ON a.service_id = s.id
                LEFT JOIN transactions t ON a.id = t.appointment_id
                WHERE a.email_hash = ?""", (email_hash,))
            appointments = cursor.fetchall()
            # Convert to list of dictionaries   
            appointments_list = []
            for row in appointments:
                appointment = {
                    "id": row[0],
                    "customer_name": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "appointment_date": row[6],
                    "end_date": row[7],
                    "special_request": row[8],
                    "receipt_id": row[9],
                    "status": row[10],
                    "service_id": row[14],
                    "service_name": row[15],
                    "service_price": row[17],
                    "payment_status": row[23] if len(row) >= 22 and row[22] else "unprocessed"
                }
                appointments_list.append(appointment)
            return jsonify(appointments_list), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
            
    pass