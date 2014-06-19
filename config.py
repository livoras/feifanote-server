# -*- coding: utf-8 -*-
import sys
DEBUG = True

if sys.argv[0] == "app.py":
    DATABASE_URI = "sqlite:///test.db"
else:
    DATABASE_URI = "sqlite:///:memory:"
ECHO = False
SECRET_KEY = '9687d209a9ff0713da8edae47dce398'
