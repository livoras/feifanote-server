# -*- coding: utf-8 -*-
import json
import config
from common import db

config.DATABASE_URI = "sqlite:///:memory:"
config.ECHO = False

def http(c, method, url, data={}):
  send_fn = getattr(c, method)
  json_data = json.dumps(data)
  headers = {'Content-Type': 'application/json'}
  return send_fn(url, headers=headers, data=json_data)
