# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
from common.utils import message, encrypt
from businesses import page
from ._helpers import require_login, notebook_ownership_check, current_user_has_notebook

api = Blueprint("page", __name__)

@api.route("/pages", methods=["POST"])
@require_login
@notebook_ownership_check
def page_action(notebook_id):
    if request.method == "POST":
        return create_new_page()

def create_new_page():
    data = request.json
    notebook_id = data.get("notebook_id")
    index = data.get("index")
    new_page = page.add_new_page(notebook_id, index)
    return jsonify(**new_page.dict()), 201 
