# -*- coding: utf-8 -*-
import json
import sqlalchemy as sc
from sqlalchemy.orm import relationship, backref

from common.db import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = sc.Column(sc.Integer, primary_key=True)
    content = sc.Column(sc.String)
    user_id = sc.Column(sc.Integer, sc.ForeignKey("users.id"))
    user = relationship("User", backref="feedbacks")

    def __init__(self, **data):
        self.__dict__.update(data)

    def dict(self):
        attrs = ("id", "content")
        return {attr: getattr(self, attr) for attr in attrs}

    def __repr__(self):
        json.dumps(self.dict())
