# -*- coding: utf-8 -*-
import config
from common import db

db.init_db()

config.DATABASE_URI = "sqlite:///:memory:"
config.ECHO = False
