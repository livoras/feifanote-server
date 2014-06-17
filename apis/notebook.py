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

@api.route("/notebooks/<notebook_id>", methods=["DELETE", "PATCH"])
@require_login
@notebook_ownership_check
def notebooks_action(notebook_id):
    if request.method == "DELETE":
        user_id = session["id"]
        notebook.delete_notebook_by_id(notebook_id)
        return message("OK.", 200)
