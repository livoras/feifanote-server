# -*- coding: utf-8 -*-
from common.db import session
from models.user import User

def is_email_existed(email):
    return session.query(User).filter_by(email=email).first()

def is_username_existed(username):
    return session.query(User).filter_by(username=username).first()

def add_new_user(user_data):
    new_user = User(**user_data)
    session.add(new_user)
    session.commit()
    return new_user

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()
