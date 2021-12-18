from flask_socketio import SocketIO
from flask import Flask
from flask_cors import CORS
import secrets

app = Flask(__name__)
CORS(app)
API = SocketIO(app, cors_allowed_origins='*')
