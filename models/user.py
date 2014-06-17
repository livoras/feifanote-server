# -*- coding: utf-8 -*-
import json
import sqlalchemy as sc
from sqlalchemy.orm import relationship, backref
from common import utils

from common.db import Base

class User(Base):
    __tablename__ = "users"

    id = sc.Column(sc.Integer, primary_key=True)
    email = sc.Column(sc.String)
    username = sc.Column(sc.String)
    password = sc.Column(sc.String)
    active_notebook_id = sc.Column(sc.Integer)

    def __init__(self, **data):
        data["password"] = utils.encrypt(data["password"])
        self.__dict__.update(data)

    def dict(self):
        attrs = ("username", "email", "id")
        return {attr: getattr(self, attr) for attr in attrs}

    def __repr__(self):
        json.dumps(self.dict())
