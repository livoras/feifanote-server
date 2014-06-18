# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
from common.utils import message, encrypt
from businesses import page
from ._helpers import require_login, \
                      notebook_ownership_check, \
                      page_ownership_check


api = Blueprint("page", __name__)

@api.route("/pages", methods=["POST"])
@require_login
@notebook_ownership_check
def create_new_page(notebook_id):
    data = request.json
    notebook_id = data.get("notebook_id")
    index = data.get("index")
    new_page = page.add_new_page(notebook_id, index)
    return jsonify(**new_page.dict()), 201 

@api.route("/pages/<page_id>", methods=["DELETE", "PATCH"])
@require_login
@page_ownership_check
def page_action(page_id):
    if request.method == "DELETE":
        page.delete_page_by_id(page_id)
        return message("OK.", 200)
    if request.method == "PATCH":
        return modify_page(page_id)

def modify_page(page_id):
    data = request.json
    if data.get("content"):
        content = data.get("content")
        page.modify_content_by_id(page_id, content)
        return message("OK.", 200)
    if data.get("index"):    
        index = data.get("index")
        page.modify_page_position(page_id, index)
        return message("OK.", 200)
    if data.get("notebook_id"):    
        return modify_page_belonging_notebook(page_id)
    return message("The field is not allowed to modify.", 400)   

@notebook_ownership_check
def modify_page_belonging_notebook(page_id, notebook_id):
    page.modify_page_belonging_notebook(page_id, notebook_id)
    return message("OK.", 200)
