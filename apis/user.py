# -*- coding: utf-8 -*-
import re
from flask import Blueprint, jsonify, request, session
from common.utils import message
from businesses import user

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
