import json
from .database import Event, User, session
from . import app
from flask import request, make_response, jsonify, render_template
from .communicate_with_db import *
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
def convert_date_to_py(date):
    return datetime.strptime(date, "%Y-%m-%d").date()
def convert_time_to_py(time):
    return datetime.strptime(time, "%H:%M").time()


def convert_request(request):
    str_request = request.decode("UTF-8")
    data_from_request = json.loads(str_request)
    user = get_jwt_identity()
    data_from_request["user"] = user
    print(data_from_request)
    return data_from_request

@app.route("/")
def main():
    return render_template("main.html")
@app.route("/create_event", methods=["POST"])
@jwt_required()
def create_event():
    data_from_request = convert_request(request.data)
    event = Event(**data_from_request)
    add_item_to_db(event)
    response = make_response({"isAdded": True})
    response.status_code = 200
    return response

@app.route("/get_events_by/<date>", methods=["GET"])
@jwt_required()
def get_events_by(date):
    print(date)
    user = get_jwt_identity()
    data = get_events_for_current_user_by(date, user)
    print(data, "data")
    response = make_response(jsonify(data))
    print(response.data)
    return response

@app.route("/login", methods=["POST"])
def login():
    request_data = json.loads(request.data)
    user = session.query(User).where(User.nickname == request_data["nickname"]).first()
    if user and check_password_hash(user.password, request_data["password"]):
        payload = {
            "user_id": user.id,
            "exp": None,
            "iat": datetime.utcnow()
        }
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))
        response = make_response({"isLogged": True, "token": token})
        response.status_code = 200
        print(response)
        return response

    response = make_response({"isLogged": False})
    response.status_code = 401
    print(response)
    return response

@app.route('/signup', methods=["POST"])
def signup():
    request_data = json.loads(request.data)
    user = session.query(User).where(User.nickname == request_data["nickname"]).first()

    if user:
        response = make_response({"isReg": False, "reason": "alr exsists"}, 409)
        return response
    password = generate_password_hash(request_data["password"])
    request_data["password"] = password
    new_user = User(**request_data)
    add_item_to_db(new_user)
    response = make_response({"isReg": True}, 200)
    return response


@app.route('/delete_user_by/<email>', methods=["POST"])
def delete_user_by(email):
    try:
        delete_user_events_by(email)
        delete_user_using(email)
        resp_data = {"IsDeleted": True}
        status_code = 200
    except:
        resp_data = {"IsDeleted": False}
        status_code = 500
    response = make_response(resp_data, status_code)
    return response

@app.route('/delete_event_by/<header>')
@jwt_required()
def delete_event_by(header):
    user = get_jwt_identity()
    try:
        delete_event_using(header, user)
        response_data = {"IsDeleted": True}
        status_code = 200
    except:
        response_data = {"IsDeleted": False}
        status_code = 409
    response = make_response(response_data, status_code)
    return response

