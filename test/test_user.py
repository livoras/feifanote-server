# -*- coding: utf-8 -*-
import json
from . import http
from app import app
from models.user import User 
from common.db import session
from common import utils
from businesses import user
from flask import session as sess

def test_signup():
    with app.test_client() as c:

        # Test for successfully user creation.
        previous_users_count = len(session.query(User).all())
        user_data = dict(
            email="jerry@163.com",
            username="lucy",
            password="123456")
        rv = http(c, "post", "/users", user_data)
        result = json.loads(rv.data)
        present_users_count = len(session.query(User).all())
        assert rv.status_code == 201
        assert present_users_count == previous_users_count + 1
        assert result["email"] == user_data["email"]
        assert result["username"] == user_data["username"]
        new_user = session.query(User).filter_by(id=result["id"]).first()
        assert new_user.password == utils.encrypt(user_data["password"])
        assert new_user.is_vip == False
        assert new_user.notebooks[0].index == 1
        assert new_user.active_notebook_id == new_user.notebooks[0].id
        assert new_user.notebooks[0].pages[0].index == 1
        assert new_user.notebooks[0].active_page_id == new_user.notebooks[0].pages[0].id
        assert len(result["notebooks"]) == 1
        assert len(result["notebooks"][0]["pages"]) == 1

        # Test for email conflicts
        user_data = dict(
            email="jerry@163.com",
            username="not-jerry",
            password="123456")
        rv = http(c, "post", "/users", user_data)
        assert rv.status_code == 409
        assert "Email has already existed." in rv.data

        # For username conflicts
        user_data = dict(
            email="iammfw-fuck@163.com",
            username="lucy",
            password="123456")
        rv = http(c, "post", "/users", user_data)
        assert rv.status_code == 409
        assert "Username has already existed." in rv.data

        user_data = dict(
            email="iammfw-fuck163.com",
            username="l",
            password="123456")
        rv = http(c, "post", "/users", user_data)
        assert rv.status_code == 400
        assert "Email is not valid." in rv.data

def test_login():
    with app.test_client() as c:
        user_data = dict(
            email="livoras@163.com",
            username="livoras",
            password="123456")
        user.add_new_user(user_data)

        with c.session_transaction() as s:
            s.clear()
        rv = http(c, "post", "/users/me", dict(email="livoras@163.com", password="123456"))
        assert rv.status_code == 200
        result = json.loads(rv.data)
        assert_attrs = ("username", "email", "id", "is_vip")
        assert sess["is_login"] == True
        for attr in assert_attrs:
            assert attr in sess
            assert sess.get(attr) == result.get(attr)

        with c.session_transaction() as s:
            s.clear()
        rv = http(c, "post", "/users/me", dict(email="livoras@me.com", password="123456"))
        assert rv.status_code == 404
        assert "User is not found." in rv.data
        assert sess.get("is_login") == None

        with c.session_transaction() as s:
            s.clear()
        rv = http(c, "post", "/users/me", dict(email="livoras@163.com", password="126"))
        assert rv.status_code == 401
        assert "Password is not correct." in rv.data
        assert sess.get("is_login") == None

def test_logout():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
        rv = http(c, "delete", "/users/me")
        assert "OK." in rv.data
        assert rv.status_code == 200
        assert not sess.get('is_login')

        with c.session_transaction() as s:
            s.clear()
        rv = http(c, "delete", "/users/me")
        assert "You have to login first." in rv.data
        assert rv.status_code == 401
