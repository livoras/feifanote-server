# -*- coding: utf-8 -*-
import json
import sqlalchemy as sc
from sqlalchemy.orm import relationship, backref

from common.db import Base

class Notebook(Base):
    __tablename__ = "notebooks"

    id = sc.Column(sc.Integer, primary_key=True)
    index = sc.Column(sc.Integer)
    user_id = sc.Column(sc.Integer, sc.ForeignKey("users.id"))
    active_page_id = sc.Column(sc.Integer, sc.ForeignKey("pages.id"))

    user = relationship("User", backref=backref("notebooks"))

    def __init__(self, **data):
        self.__dict__.update(data)

    def dict(self):
        return {}

    def __repr__(self):
        json.dumps(self.dict())
