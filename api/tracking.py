from flask import request
from flask_socketio import emit
# api/tracking.py
clients = {}

def handle_connect(socketio):
    try:
        session_id = request.sid
        clients[session_id] = request.remote_addr  # Optionally, store IP or any other info
        print("Remote address:", request.sid)
        print(f"Client connected: {session_id} from {clients[session_id]}")
    except Exception as e:
        print(f"Error handling connection: {e}")

def handle_message(socketio, data):
    try:

        sender_session_id = request.sid
        print(f"Received message: {data} from {sender_session_id}")

        for session_id in clients:
            if session_id != sender_session_id:
                print("Sending message to:", session_id)
                # Send a message to all clients except the sender
                socketio.send(data, to=session_id, namespace="/track_navigator")
    except Exception as e:
        print(f"Error handling message: {e}")

def handle_disconnect(socketio):
    try:
        session_id = request.sid
        if session_id in clients:
            del clients[session_id]  
            print(f"Client disconnected: {session_id}")
    except Exception as e:
        print(f"Error handling disconnection: {e}")

