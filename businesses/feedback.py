# -*- coding: utf-8 -*-
from models.feedback import Feedback
from common.db import session

def create_feedback(feedback_data):
    session.add(Feedback(**feedback_data))
    session.commit()
