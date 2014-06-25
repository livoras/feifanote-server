# -*- coding: utf-8 -*-
import json
from . import http
from app import app
from common.db import session
from common import utils
from flask import session as sess
from models.feedback import Feedback

def test_create_feedback():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        rv = http(c, "post", "/feedbacks", dict(content="FUCKYOU"))
        assert "OK." in rv.data
        assert rv.status_code == 201
        feedback = session.query(Feedback).first()
        assert feedback.content == "FUCKYOU"
