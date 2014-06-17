# -*- coding: utf-8 -*-
import re
from flask import Blueprint, jsonify, request, session
from common.utils import message, encrypt
from businesses import user
from ._helpers import require_login

api = Blueprint("user", __name__)

@api.route("/users", methods=["POST"])
def signup():
    data = request.json
    validation = check_user_data_validation(data)
    if not validation[0]:
        return message(validation[1], 400)
    if user.is_email_existed(data["email"]):    
        return message("Email has already existed.", 409)
    if user.is_username_existed(data["username"]):
        return message("Username has already existed.", 409)
    new_user = user.add_new_user(data)
    return jsonify(new_user.dict()), 201

def check_user_data_validation(user_data):
    to_check_attrs = ("username", "email", "password")
    for attr in to_check_attrs:
        if not attr in user_data:
            return False, "%s is required" % attr
    if not 0 < len(user_data["username"]) <= 30:
        return False, "Username is not valid."
    if not is_email_valid(user_data["email"]):
        return False, "Email is not valid."
    if not 6 <= len(user_data["password"]) <= 30:
        return False, "Password is not valid."
    return True,

def is_email_valid(email):
    return re.match("\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*", email)

@api.route("/user/me", methods=["POST", "DELETE"])
def user_actions():
    if request.method == "POST":
        return login()
    elif request.method == "DELETE":    
        return logout()

def login():
    data = request.json
    current_user = user.get_user_by_email(data.get("email"))
    if not current_user:
        return message("User is not found.", 404)
    if not current_user.password == encrypt(data.get("password")):
        return message("Password is not correct.", 401)
    session["is_login"] = True
    for to_set in ("username", "email", "id"):
        session[to_set] = getattr(current_user, to_set)
    return jsonify(**current_user.dict()), 200    

@require_login
def logout():
    session.clear()
    return message("OK.", 200)
