# -*- coding: utf-8 -*-
from common.db import session
from models.user import User
from businesses import notebook

def is_email_existed(email):
    return session.query(User).filter_by(email=email).first()

def is_username_existed(username):
    return session.query(User).filter_by(username=username).first()

def add_new_user(user_data):
    new_user = User(**user_data)
    session.add(new_user)
    session.commit()
    notebook_data = dict(
        name=new_user.username,
        user_id=new_user.id,
        index=1)
    new_notebook = notebook.add_new_notebook(notebook_data)
    new_user.active_notebook_id = new_notebook.id
    session.commit()
    return new_user, new_notebook

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def get_user_by_id(id):
    return session.query(User).filter_by(id=id).first()
