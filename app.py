# -*- coding: utf-8 -*-
from flask import Flask
import config
from common.db import init_db

app = Flask(__name__)
app.config.from_object(config)

def init_apis():
    from apis import apis
    for api in apis:
        app.register_blueprint(api)

def cros(response):
    headers = (
        'Access-Control-Allow-Origin', 
        'Access-Control-Allow-Methods')
    for header in headers:
        response.headers[header] = '*'
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"   
    return response

init_apis()
init_db()

if __name__ == "__main__":
    if config.DEBUG:
        app.process_response = cros
    app.run()
