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

def test_delete_a_notebook():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        to_delete_notebook = session.query(Notebook).filter_by(user_id=2, index=25).first()
        previous_cout = len(session.query(Notebook) \
            .filter(
                Notebook.user_id==2,
                Notebook.index>=to_delete_notebook.index) \
            .all())
        rv = http(c, "delete", "/notebooks/%s" % to_delete_notebook.id)
        assert rv.status_code == 200
        assert "OK." in rv.data
        current_count = len(session.query(Notebook) \
            .filter(
                Notebook.user_id==2,
                Notebook.index>to_delete_notebook.index) \
            .all())
        assert current_count == previous_cout - 2

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        to_delete_notebook = session.query(Notebook).filter_by(user_id=1).first()
        rv = http(c, "delete", "/notebooks/%s" % to_delete_notebook.id)
        assert rv.status_code == 404
        assert "Notebook is not found." in rv.data

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        rv = http(c, "delete", "/notebooks/3000000")
        assert rv.status_code == 404
        assert "Notebook is not found." in rv.data

def test_modify_notebook_name():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        to_modify_notebook = session.query(Notebook).filter_by(user_id=2).first()
        notebook_id = to_modify_notebook.id
        rv = http(c, "patch", "/notebooks/%s?field=name" % notebook_id, dict(name="new_notebook_name"))
        assert rv.status_code == 200
        to_modify_notebook = session.query(Notebook).filter_by(user_id=2).first()
        assert to_modify_notebook.name == "new_notebook_name"
