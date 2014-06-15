# -*- coding: utf-8 -*-
import json
import sqlalchemy as sc
from sqlalchemy.orm import relationship, backref

from common.db import Base

class User(Base):
    __tablename__ = "users"

    id = sc.Column(sc.Integer, primary_key=True)
    email = sc.Column(sc.String)
    username = sc.Column(sc.String)
    active_notebook_id = sc.Column(sc.Integer)

    def __init__(self, **data):
        self.__dict__.update(data)

    def dict(self):
        return {}

    def __repr__(self):
        json.dumps(self.dict())
