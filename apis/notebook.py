# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import re
from flask import Blueprint, jsonify, request, session
from common.utils import message, encrypt
from businesses import notebook
from ._helpers import require_login, notebook_ownership_check

api = Blueprint("notebook", __name__)

@api.route("/notebooks", methods=["POST"])
@require_login
def create_new_notebook():
    data = request.json
    validation = check_notebook_data_valid(data)
    if not validation[0]:
        return message(validation[1], 400)
    user_id = session.get("id")
    if notebook.find_notebook_by_name_with_user_id(data["name"], user_id):
        return message("Name has already existed.", 409)
    data["user_id"] = user_id
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

@api.route("/notebooks/<notebook_id>", methods=["DELETE", "PATCH"])
@require_login
@notebook_ownership_check
def notebooks_action(notebook_id):
    if request.method == "DELETE":
        user_id = session["id"]
        notebook.delete_notebook_by_id(notebook_id)
        return message("OK.", 200)
    elif request.method == "PATCH":
        data = request.json
        if data.get("name"):
            new_name = data.get("name")
            return modify_notebook_name(notebook_id, new_name)
        if data.get("index"):    
            new_index = data.get("index")
            notebook.modify_notebook_position(notebook_id, new_index)
            return message("OK.", 200)
        return message("The filed is not allowed."), 400

def modify_notebook_name(notebook_id, name):
    user_id = session.get("id")
    if len(name) == 0:
        return message("Name is not valid.", 400)
    to_modify_notebook = notebook.find_notebook_by_name_with_user_id(name, user_id)
    if to_modify_notebook:
        return message("Name has already existed.", 409)
    notebook.modify_notebook_name(notebook_id, name)
    return message("OK.", 200)
