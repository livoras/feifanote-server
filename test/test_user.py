# -*- coding: utf-8 -*-
from app import app

def test_signup():
    with app.test_client() as c:
        rv = c.get('/user/signup')
        assert 'jerry' in rv.data
