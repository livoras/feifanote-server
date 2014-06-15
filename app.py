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

init_db()
init_apis()

if __name__ == "__main__":
    app.run()
