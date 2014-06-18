# -*- coding: utf-8 -*-
from functools import wraps
from flask import session, request
from common.utils import message
from models.notebook import Notebook
from models.page import Page
from common import db

def require_login(route_fn):
    """
    Decorator for router functions that need user to login first.
    """
    @wraps(route_fn)
    def _require_login(*argvs, **keywords):
        if not session.get("is_login"):
            return message("You have to login first.", 401)
        else:    
            return route_fn(*argvs, **keywords)
    return _require_login        

def notebook_ownership_check(route_fn):
    @wraps(route_fn)
    def _route_fn(*argvs, **keywords):
        data = request.json
        notebook_id = data.get("notebook_id")
        notebook_id = notebook_id or keywords.get("notebook_id")
        not_found = message("Notebook is not found.", 404)
        if not session.get("is_login"):
            return not_found 
        if not current_user_has_notebook(notebook_id):
            return not_found
        keywords.setdefault("notebook_id", notebook_id)
        return route_fn(*argvs, **keywords)
    return _route_fn    

def current_user_has_notebook(notebook_id):
    user_id = session.get("id")
    notebook = db.session.query(Notebook) \
                         .filter_by(id=notebook_id, user_id=user_id) \
                         .first()
    return notebook

def page_ownership_check(route_fn):
    @wraps(route_fn)
    def _route_fn(*argvs, **keywords):
        data = request.json
        page_id = data.get("page_id")
        page_id = page_id or keywords.get("page_id")
        page = db.session.query(Page).filter_by(id=page_id).first()
        if not page or page.notebook.user_id != session.get("id"):
            return message("Page is not found.", 404)
        keywords.setdefault("page_id", page_id)
        return route_fn(*argvs, **keywords)
    return _route_fn