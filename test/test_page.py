# -*- coding: utf-8 -*-
import json
from flask import session as sess
from . import http
from app import app
from models.user import User 
from models.notebook import Notebook
from models.page import Page
from common.db import session
from common import utils
from businesses import user

user_id = None
notebook_id = None

def setup():
    global user_id
    global notebook_id
    new_user = User(**dict(password="123465"))
    session.add(new_user)
    session.commit()
    user_id = new_user.id
    for index in xrange(1, 51):
        new_notebook = Notebook(**dict(
            user_id=user_id,
            name="notebook_name_of_%s" % user_id,
            index=index))
        session.add(new_notebook)
    session.commit()
    notebook_id = new_notebook.id
    for index in xrange(1, 51):
        new_page = Page(**dict(
            notebook_id=notebook_id,
            content="page_content",
            index=index))
        session.add(new_page)
    session.commit()

def test_create_page():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s.clear()
        rv = http(c, "post", "/pages", dict(notebook_id=notebook_id, index=1))
        assert rv.status_code == 401
        assert "You have to login first." in rv.data

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 1
        rv = http(c, "post", "/pages", dict(notebook_id=notebook_id, index=1))
        assert rv.status_code == 404
        assert "Notebook is not found." in rv.data

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = user_id
        previous_count = len(session.query(Page).filter_by(notebook_id=notebook_id).all())
        rv = http(c, "post", "/pages", dict(notebook_id=notebook_id, index=1))
        current_count = len(session.query(Page).filter_by(notebook_id=notebook_id).all())
        assert rv.status_code == 201
        assert "id" in rv.data
        assert "index" in rv.data
        assert current_count == previous_count + 1

def test_delete_page():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = user_id
        new_page = Page(**dict(notebook_id=1))    
        session.add(new_page)
        session.commit()
        rv = http(c, "delete", "/pages/%s" % new_page.id)
        assert rv.status_code == 404
        assert "Page is not found." in rv.data

    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = user_id
        to_delete_page = session.query(Page).filter_by(notebook_id=notebook_id).first()    
        previous_count = len(session.query(Page).filter_by(notebook_id=notebook_id).all())
        rv = http(c, "delete", "/pages/%s" % to_delete_page.id)
        current_count = len(session.query(Page).filter_by(notebook_id=notebook_id).all())
        assert rv.status_code == 200
        assert "OK." in rv.data
        assert current_count == previous_count - 1

def test_save_content_of_page():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = user_id
        to_modify_page = session.query(Page).filter_by(notebook_id=notebook_id).first()
        page_id = to_modify_page.id
        rv = http(c, "patch", "/pages/%s" % page_id, dict(content="FUCKYOU"))
        newer_page = session.query(Page).filter_by(id=page_id).first()
        assert rv.status_code == 200
        assert "OK." in rv.data
        assert "FUCKYOU" == newer_page.content

def test_modify_page_position():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = user_id
        to_modify_page = session.query(Page).filter_by(notebook_id=notebook_id).first()
        page_id = to_modify_page.id
        rv = http(c, "patch", "/pages/%s" % page_id, dict(index=25))
        newer_page = session.query(Page).filter_by(id=page_id).first()
        assert rv.status_code == 200
        assert newer_page.index == 25
        assert "OK." in rv.data
