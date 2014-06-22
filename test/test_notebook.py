# -*- coding: utf-8 -*-
import json
from . import http
from app import app
from common.db import session
from common import utils
from flask import session as sess
from models.notebook import Notebook
from models.user import User

def setup():
    session.add(User(**dict(password="123465")))
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
        notebook = session.query(Notebook).filter_by(user_id=2, index=1).first()
        assert notebook.name == "notebook_name2"
        assert notebook.pages[0].index == 1
        assert notebook.active_page_id == notebook.pages[0].id
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

        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        to_modify_notebook = session.query(Notebook).filter_by(user_id=2).all()[2]
        notebook_id = to_modify_notebook.id
        rv = http(c, "patch", "/notebooks/%s?field=name" % notebook_id, dict(name="new_notebook_name"))
        assert rv.status_code == 409
        to_modify_notebook = session.query(Notebook).filter_by(user_id=2).first()
        assert to_modify_notebook.name == "new_notebook_name"

        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        to_modify_notebook = session.query(Notebook).filter_by(user_id=1).first()
        notebook_id = to_modify_notebook.id
        rv = http(c, "patch", "/notebooks/%s?field=name" % notebook_id, dict(name="new_notebook_name1"))
        assert rv.status_code == 404
        assert "Notebook is not found." in rv.data

        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 1
        rv = http(c, "patch", "/notebooks/2304314321?field=name", dict(name="new_notebook_name1"))
        assert rv.status_code == 404
        assert "Notebook is not found." in rv.data

def test_modify_notebook_position():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        notebooks = session.query(Notebook).filter_by(user_id=2).all()
        # simulate 25 -> 10
        to_move_index = 25
        target_index = 10
        id_of_target_pos = session.query(Notebook).filter_by(user_id=2, index=target_index).first().id
        id_of_previous_pos = session.query(Notebook).filter_by(user_id=2, index=to_move_index-1).first().id
        id_of_to_move = session.query(Notebook).filter_by(user_id=2, index=to_move_index).first().id
        rv = http(c, "patch", "/notebooks/%s" % id_of_to_move, dict(index=target_index))
        assert "OK." in rv.data
        notebook_of_target_pos = session.query(Notebook).filter_by(id=id_of_target_pos).first()
        notebook_of_previous_pos = session.query(Notebook).filter_by(id=id_of_previous_pos).first()
        notebook_of_to_move = session.query(Notebook).filter_by(id=id_of_to_move).first()
        assert notebook_of_target_pos.index == target_index + 1
        assert notebook_of_previous_pos.index == to_move_index
        assert notebook_of_to_move.index == target_index

        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        notebooks = session.query(Notebook).filter_by(user_id=2).all()
        # simulate 20 -> 30
        to_move_index = 20
        target_index = 30
        id_of_target_pos = session.query(Notebook).filter_by(user_id=2, index=target_index).first().id
        id_of_next_pos = session.query(Notebook).filter_by(user_id=2, index=to_move_index+1).first().id
        id_of_to_move = session.query(Notebook).filter_by(user_id=2, index=to_move_index).first().id
        rv = http(c, "patch", "/notebooks/%s" % id_of_to_move, dict(index=target_index))
        assert "OK." in rv.data
        notebook_of_target_pos = session.query(Notebook).filter_by(id=id_of_target_pos).first()
        notebook_of_next_pos = session.query(Notebook).filter_by(id=id_of_next_pos).first()
        notebook_of_to_move = session.query(Notebook).filter_by(id=id_of_to_move).first()
        assert notebook_of_target_pos.index == target_index - 1
        assert notebook_of_next_pos.index == to_move_index
        assert notebook_of_to_move.index == target_index

def test_retrieve_all_notebooks():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        rv = http(c, "get", "/notebooks")    
        result = json.loads(rv.data)
        all_notebooks = session.query(Notebook).filter_by(user_id=2).all()
        assert len(result["notebooks"]) == len(all_notebooks)

def test_retrieve_specific_notebook():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        to_get = session.query(Notebook).filter_by(user_id=2).first()
        rv = http(c, "get", "/notebooks/%s" % to_get.id)    
        assert to_get.name in rv.data
        assert "pages" in rv.data
        assert rv.status_code == 200

def test_change_active_notebook():
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["is_login"] = True
            s["id"] = 2
        to_set_id = session.query(Notebook).filter_by(user_id=2).first().id
        rv = http(c, "put", "/notebooks/active_notebook", dict(notebook_id=to_set_id))
        assert session.query(User).filter_by(id=2).first().active_notebook_id == to_set_id
        assert "OK." in rv.data
