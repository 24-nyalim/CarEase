from flask_cors import CORS
from flask import Flask, render_template
from views import bp as views_bp
from api import bp as api_bp, tracking
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='templates', static_folder='static')

# Enable CORS for all domains
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(views_bp)
app.register_blueprint(api_bp)

socketio = SocketIO(app)  # Initialize globally

@socketio.on("connect", namespace="/track_navigator")
def handle_connect():
    tracking.handle_connect(socketio)  # Call the function from tracking.py

@socketio.on("message", namespace="/track_navigator")
def handle_message(data):
    tracking.handle_message(socketio, data)

@socketio.on("disconnect", namespace="/track_navigator")
def handle_disconnect():
    tracking.handle_disconnect(socketio)  # Call the function from tracking.py


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True, allow_unsafe_werkzeug=True)