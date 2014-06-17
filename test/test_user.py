# -*- coding: utf-8 -*-
import json
from . import http
from app import app
from models.user import User 
from common.db import session
from common import utils

def test_signup():
    with app.test_client() as c:

        # Test for successfully user creation.
        previous_users_count = len(session.query(User).all())
        user_data = dict(
            email='jerry@163.com',
            username='lucy',
            password='123456')
        rv = http(c, 'post', '/users', user_data)
        result = json.loads(rv.data)
        present_users_count = len(session.query(User).all())
        assert rv.status_code == 201
        assert present_users_count == previous_users_count + 1
        assert result['email'] == user_data['email']
        assert result['username'] == user_data['username']
        new_user = session.query(User).filter_by(id=result["id"]).first()
        assert new_user.password == utils.encrypt(user_data["password"])

        # Test for email conflicts
        user_data = dict(
            email='jerry@163.com',
            username='not-jerry',
            password='123456')
        rv = http(c, 'post', '/users', user_data)
        assert rv.status_code == 409
        assert 'Email has already existed.' in rv.data

        # For username conflicts
        user_data = dict(
            email='iammfw-fuck@163.com',
            username='lucy',
            password='123456')
        rv = http(c, 'post', '/users', user_data)
        assert rv.status_code == 409
        assert 'Username has already existed.' in rv.data

        user_data = dict(
            email='iammfw-fuck163.com',
            username='l',
            password='123456')
        rv = http(c, 'post', '/users', user_data)
        assert rv.status_code == 400
        assert 'Email is not valid.' in rv.data
