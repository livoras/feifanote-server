# -*- coding: utf-8 -*-
from app import app

def test_signup():
    with app.test_client() as c:
        rv = c.get('/user/signup')
        app.logger.debug(rv.data)
        assert 'jerry' in rv.data
