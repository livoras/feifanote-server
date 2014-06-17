# -*- coding: utf-8 -*-
from functools import wraps
from flask import session
from common.utils import message
from models.notebook import Notebook
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
    def _route_fn(notebook_id):
        not_found = message("Notebook is not found.", 404)
        if not session.get("is_login"):
            return not_found 
        notebook = db.session.query(Notebook).filter_by(id=notebook_id).first()
        if not notebook or notebook.user_id != session.get("id"):
            return not_found
        return route_fn(notebook_id)    
    return _route_fn    
