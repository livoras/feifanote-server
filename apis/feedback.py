# -*- coding: utf-8 -*-
import re
from flask import Blueprint, jsonify, request, session, make_response
from common.utils import message
from businesses import feedback
from ._helpers import require_login

api = Blueprint("feedback", __name__)

@api.route("/feedbacks", methods=["POST"])
@require_login
def create_feedback():
    data = request.json
    content = data.get("content")
    if not content or len(content) == 0:
        return message("Content is not empty.", 400)
    data["user_id"] = session["id"]
    feedback.create_feedback(data)
    return message("OK.", 201)

@api.route("/feedbacks/<int:start>/<int:end>", methods=["GET"])
def get_feedbacks(start, end):
  feedbacks = feedback.get_feedbacks(start, end)
  result = "<ul>"
  for fb in feedbacks:
    result = result + "<li><b>%s</b> said: <i>%s</i></li><hr>" % (fb.user.email, fb.content)
  result = result + "</ul>"
  return result
