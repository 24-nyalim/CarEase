from flask import request, jsonify
import requests
import os
import base64
from . import bp  # import the Blueprint instance
from datetime import datetime
import sqlite3
from dotenv import load_dotenv

load_dotenv()

SHORTCODE = "174379"  # Daraja sandbox shortcode


def _daraja_base_url():
    env = (os.getenv("MPESA_ENV") or "sandbox").strip().lower()
    if env == "production":
        return "https://api.safaricom.co.ke", env
    return "https://sandbox.safaricom.co.ke", "sandbox"


def _get_daraja_config():
    consumer_key = (os.getenv("MPESA_CONSUMER_KEY") or "").strip()
    consumer_secret = (os.getenv("MPESA_CONSUMER_SECRET") or "").strip()
    passkey = (os.getenv("MPESA_PASSKEY") or "").strip()
    callback_url = (os.getenv("CALLBACK_URL") or "").strip()

    missing = []
    if not consumer_key:
        missing.append("MPESA_CONSUMER_KEY")
    if not consumer_secret:
        missing.append("MPESA_CONSUMER_SECRET")
    if not passkey:
        missing.append("MPESA_PASSKEY")
    if not callback_url:
        missing.append("CALLBACK_URL")

    if missing:
        raise ValueError(f"Missing Daraja configuration in .env: {', '.join(missing)}")

    return consumer_key, consumer_secret, passkey, callback_url


def _normalize_amount(value):
    if value is None:
        return 1
    cleaned = str(value).strip().replace("$", "").replace(",", "")
    try:
        parsed = int(float(cleaned))
    except (TypeError, ValueError):
        return 1
    return max(parsed, 1)


def get_access_token():
    consumer_key, consumer_secret, _, _ = _get_daraja_config()
    base_url, env = _daraja_base_url()
    auth_url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
        auth_url,
        auth=(consumer_key, consumer_secret),
        headers={"Accept": "application/json"},
        timeout=20,
    )

    try:
        body = response.json()
    except ValueError:
        body = {"raw": response.text}

    if response.status_code == 200 and isinstance(body, dict) and body.get("access_token"):
        return body.get("access_token")

    if isinstance(body, dict):
        error_message = body.get("error_description") or body.get("errorMessage") or body.get("error") or body
    else:
        error_message = body
    raise RuntimeError(
        f"Failed to get Daraja access token ({response.status_code}, {env}): {error_message}"
    )

@bp.route("/stk_push", methods=["POST"])
def stk_push():
    """Initiate an STK Push request."""
    data = request.json  # Get JSON data from frontend
    phone_number = data.get("phone")
    appointment_id = data.get("appointment_id")
    amount = _normalize_amount(data.get("amount", 1))

    if not phone_number or not appointment_id:
        return jsonify({"error": "Phone number and receipt ID are required"}), 400

    try:
        _, _, passkey, callback_url = _get_daraja_config()
        access_token = get_access_token()
        base_url, _ = _daraja_base_url()
        stk_url = f"{base_url}/mpesa/stkpush/v1/processrequest"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Correct Password Encoding: Base64(SHORTCODE + PASSKEY + TIMESTAMP)
    password = base64.b64encode(f"{SHORTCODE}{passkey}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,  # Corrected password
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # Customer's phone number
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "TestPayment",
        "TransactionDesc": "Payment for service"
    }
    try:
        response = requests.post(stk_url, json=payload, headers=headers, timeout=30)
        body = response.json()
    except ValueError:
        return jsonify({"error": "Daraja returned a non-JSON response"}), 502
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to call Daraja STK API: {str(e)}"}), 502

    if response.status_code >= 400:
        return jsonify({
            "error": f"Daraja STK request failed ({response.status_code})",
            "details": body
        }), response.status_code

    print("STK Push Response:", body)  # Debugging output

    if body.get("ResponseCode") == "0":

        with sqlite3.connect("db/CarEase.db") as conn:
            cursor = conn.cursor()
            try:
                # Insert the transaction into the database
                cursor.execute("""
                    INSERT INTO transactions (appointment_id, amount, payment_method, status, reference_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (appointment_id, amount, "mpesa", "pending", body.get("CheckoutRequestID")))
                conn.commit()
            except sqlite3.Error as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"status": "success", "data": body}), 200
    else:
        return jsonify({"status": "failed", "data": body}), 400


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
            if str(ResultCode) == "0":
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
