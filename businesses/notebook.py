# -*- coding: utf-8 -*-
from models.notebook import Notebook
from common.db import session

def find_notebook_by_name(name):
    return session.query(Notebook).filter_by(name=name).first()

def add_new_notebook(notebook_data):
    new_notebook = Notebook(**notebook_data)
    user_id, index = notebook_data["user_id"], notebook_data["index"]
    shift_notebooks_front_from(user_id, index)
    session.add(new_notebook)
    session.commit()
    return new_notebook

def shift_notebooks_front_from(user_id, index):
    to_shift_notebooks = session.query(Notebook).filter(
        Notebook.user_id==user_id,
        Notebook.index>=index)
    for notebook in to_shift_notebooks:
        notebook.index += 1
    session.commit()

def delete_notebook_by_id(notebook_id):
    to_delete_notebook = session.query(Notebook) \
                                .filter_by(id=notebook_id) \
                                .first()
    user_id = to_delete_notebook.user_id
    index = to_delete_notebook.index
    session.delete(to_delete_notebook)
    session.commit()
    shift_notebooks_back_from(user_id, index)

def shift_notebooks_back_from(user_id, index):
    to_shift_notebooks = session.query(Notebook).filter(
        Notebook.user_id==user_id,
        Notebook.index>index)
    for notebook in to_shift_notebooks:
        notebook.index -= 1
    session.commit()
