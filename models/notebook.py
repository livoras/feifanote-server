# -*- coding: utf-8 -*-
import json
import sqlalchemy as sc
from sqlalchemy.orm import relationship, backref

from common.db import Base

class Notebook(Base):
    __tablename__ = "notebooks"

    id = sc.Column(sc.Integer, primary_key=True)
    index = sc.Column(sc.Integer)
    name = sc.Column(sc.String)
    active_page_id = sc.Column(sc.Integer, default=-1)
    user_id = sc.Column(sc.Integer, sc.ForeignKey("users.id"))

    user = relationship("User", backref=backref("notebooks"))

    def __init__(self, **data):
        self.__dict__.update(data)

    def dict(self):
        attrs = ("name", "index", "active_page_id", "user_id")
        return {attr: getattr(self, attr) for attr in attrs}

    def __repr__(self):
        return json.dumps(self.dict())
