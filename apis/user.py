# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session

api = Blueprint('user', __name__)

@api.route('/user/signup')
def signup():
    result = dict(name="jerry")
    return jsonify(**result)
