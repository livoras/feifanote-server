# -*- coding: utf-8 -*-
import json
from . import http
from app import app
from common.db import session
from common import utils
from flask import session as sess
from models.notebook import Notebook

def setup():
    for index in xrange(1, 51):
        new_notebook = Notebook(**dict(
            user_id=2,
            name="notebook_name",
            index=index))
        session.add(new_notebook)
    session.commit()

def test_create_a_notebook():
    assert len(session.query(Notebook).filter_by(user_id=2).all()) == 50
    assert len(session.query(Notebook).filter(Notebook.user_id==2, Notebook.index>=26).all()) == 25

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        rv = http(c, "post", "/notebooks", dict(
            name="notebook_name2",
            index=1))
        assert rv.status_code == 201
        assert len(session.query(Notebook).filter(Notebook.user_id==2).all()) == 51
        assert len(session.query(Notebook).filter(Notebook.user_id==2, Notebook.index > 1).all()) == 50
        assert session.query(Notebook).filter_by(user_id=2, index=1).first().name == "notebook_name2"
        assert "name" in rv.data

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        rv = http(c, "post", "/notebooks", dict(
            name="notebook_name2",
            index=1))
        assert rv.status_code == 409
        assert "Name has already existed." in rv.data

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        rv = http(c, "post", "/notebooks", dict(index=1))
        assert rv.status_code == 400
        assert "Name is not valid." in rv.data
