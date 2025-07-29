from flask import Flask, request, jsonify
import requests
import os
import base64
from . import bp  # import the Blueprint instance
from datetime import datetime
import sqlite3

app = Flask(__name__)

CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
SHORTCODE = "174379"  # Test Paybill
CALLBACK_URL = os.getenv("CALLBACK_URL")  # Your callback URL
PASSKEY= os.getenv("MPESA_PASSKEY")  # Your passkey

def get_access_token():
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # Encode Consumer Key and Secret in Base64
    credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(auth_url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error:", response.json())  # Debugging output
        return None

@bp.route("/stk_push", methods=["POST"])
def stk_push():
    """Initiate an STK Push request."""
    data = request.json  # Get JSON data from frontend
    phone_number = data.get("phone")
    appointment_id = data.get("appointment_id")
    amount = data.get("amount", 1)  # Default to 1 if not provided

    if not phone_number or not appointment_id:
        return jsonify({"error": "Phone number and receipt ID are required"}), 400
    
    # Get Access Token
    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to get access token"}), 500

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Correct Password Encoding: Base64(SHORTCODE + PASSKEY + TIMESTAMP)
    password = base64.b64encode(f"{SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,  # Corrected password
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone_number,  # Customer's phone number
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "TestPayment",
        "TransactionDesc": "Payment for service"
    }

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    response = requests.post(stk_url, json=payload, headers=headers)
    print("STK Push Response:", response.json())  # Debugging output
    if response.json().get("ResponseCode") == "0":

        with sqlite3.connect("db/CarEase.db") as conn:
            cursor = conn.cursor()
            try:
                # Insert the transaction into the database
                cursor.execute("""
                    INSERT INTO transactions (appointment_id, amount, payment_method, status, reference_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (appointment_id, amount, "mpesa", "pending", response.json().get("CheckoutRequestID")))
                conn.commit()
            except sqlite3.Error as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"status": "success", "data": response.json()}), 200
    else:
        return jsonify(response.json())


@bp.route("/dapi_callback", methods=["POST"])
def dapi_callback():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    # Safely access values to prevent KeyErrors
    stk_callback = data.get("Body", {}).get("stkCallback", {})
    CheckoutRequestID = stk_callback.get("CheckoutRequestID")
    ResultCode = stk_callback.get("ResultCode")

    if not CheckoutRequestID or ResultCode is None:
        return jsonify({"error": "Missing required fields"}), 400

    print(f"Received callback: CheckoutRequestID={CheckoutRequestID}, ResultCode={ResultCode}")
    
    with sqlite3.connect("db/CarEase.db") as conn:
        cursor = conn.cursor()
        try:
            # Update the transaction status in the database
            if ResultCode == 0:
                cursor.execute("""
                    UPDATE transactions SET status = ? WHERE reference_id = ?
                """, ("completed", CheckoutRequestID))
            else:
                cursor.execute("""
                    UPDATE transactions SET status = ? WHERE reference_id = ?
                """, ("failed", CheckoutRequestID))
                conn.commit()
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    # Process the callback data here
    # For example, save the transaction status to the database
    print(data)
    return jsonify({"status": "success", "data": data}), 200