# -*- coding: utf-8 -*-
import json
import sqlalchemy as sc
from sqlalchemy.orm import relationship, backref

from common.db import Base

class Page(Base):
    __tablename__ = "pages"

    id = sc.Column(sc.Integer, primary_key=True)
    index = sc.Column(sc.Integer)
    content = sc.Column(sc.String)
    notebook_id = sc.Column(sc.Integer, sc.ForeignKey("notebooks.id"))

    notebook = relationship("Notebook", backref=backref("pages"))

    def __init__(self, **data):
        self.__dict__.update(data)

    def dict(self):
        return {}

    def __repr__(self):
        json.dumps(self.dict())
