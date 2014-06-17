# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import re
from flask import Blueprint, jsonify, request, session
from common.utils import message, encrypt
from businesses import notebook
from ._helpers import require_login

api = Blueprint("notebook", __name__)

@api.route("/notebooks", methods=["POST"])
@require_login
def create_new_notebook():
    data = request.json
    validation = check_notebook_data_valid(data)
    if not validation[0]:
        return message(validation[1], 400)
    if notebook.find_notebook_by_name(data["name"]):
        return message("Name has already existed.", 409)
    data["user_id"] = session.get("id")   
    new_notebook = notebook.add_new_notebook(data)    
    return jsonify(**new_notebook.dict()), 201

def check_notebook_data_valid(data):
    name = data.get("name")
    index = data.get("index")
    if not name or len(name) > 30 or len(name) == 0:
        return False, "Name is not valid."
    if not isinstance(index, int):
        return False, "Index is not valid."
    return True,
