# -*- coding: utf-8 -*-
import os
import json
from flask import Flask, request, \
                  render_template, \
                  send_file, \
                  session
import config
from common.db import init_db

app = Flask(__name__, template_folder="feifanote")
app.config.from_object(config)

@app.route('/')
def index():
    init_data = get_init_data()
    if config.DEBUG:
        return render_template("index.html", init_data=init_data)
    else:
        return render_template("index-optimalize.html", init_data=init_data)

def get_init_data():
    if not session.get("is_login"):
        return json.dumps(dict(is_login=False))
    attrs = (
        "username", 
        "email", "id", 
        "is_vip", 
        "active_notebook_id")
    user = {attr: session.get(attr) for attr in attrs}
    return json.dumps(dict(is_login=True, user=user))

@app.errorhandler(404)
def check_static(error):
    path = 'feifanote' + request.path
    data = dict(notification="")
    if os.path.exists(path):
        return send_file(path)
    else:  
        return render_template('404.html', **data), 404

def init_apis():
    from apis import apis
    for api in apis:
        app.register_blueprint(api)

init_apis()
init_db()

if __name__ == "__main__":
    app.run()
