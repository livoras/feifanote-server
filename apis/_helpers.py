# -*- coding: utf-8 -*-
from functools import wraps
from flask import session
from common.utils import message

def require_login(route_fn):
    """
    Decorator for router functions that need user to login first.
    """
    @wraps(route_fn)
    def _require_login():
        if not session.get("is_login"):
            return message("You have to login first.", 401)
        else:    
            return route_fn()
    return _require_login        
