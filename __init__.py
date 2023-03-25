from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = "sEcReT"
app.config["JWT_SECRET_KEY"] = "super-secret"
CORS(app)
JWTManager(app)

from api.login_service import *
from . import endpoint
