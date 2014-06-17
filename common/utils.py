# -*- coding: utf-8 -*-
import hashlib
from flask import jsonify

def message(msg, status_code, headers=None):
    return jsonify(dict(message=msg)), status_code, headers

def encrypt(string):
  crypt = hashlib.sha256()
  crypt.update(string)
  return crypt.hexdigest()
