# -*- coding: utf-8 -*-
from models.notebook import Notebook
from models.user import User
from common.db import session
from sys import maxint

def find_notebook_by_name_with_user_id(name, user_id):
    return session.query(Notebook) \
                  .filter_by(name=name, user_id=user_id) \
                  .first()

def add_new_notebook(notebook_data):
    user_id, index = notebook_data["user_id"], notebook_data["index"]
    shift_notebooks(user_id, index, maxint)
    new_notebook = Notebook(**notebook_data)
    session.add(new_notebook)
    session.commit()
    return new_notebook

def delete_notebook_by_id(notebook_id):
    to_delete_notebook = session.query(Notebook) \
                                .filter_by(id=notebook_id) \
                                .first()
    user_id = to_delete_notebook.user_id
    index = to_delete_notebook.index
    session.delete(to_delete_notebook)
    session.commit()
    shift_notebooks(user_id, index + 1, maxint, True)

def shift_notebooks(user_id, _from, to, back=False):
    to_shift_notebooks = session.query(Notebook).filter(
        Notebook.user_id==user_id,
        Notebook.index>=_from,
        Notebook.index<to)
    for notebook in to_shift_notebooks:
        if back:
            notebook.index -= 1
        else:    
            notebook.index += 1
    session.commit()

def modify_notebook_name(notebook_id, name):
    notebook = session.query(Notebook).filter_by(id=notebook_id).first()
    notebook.name = name
    session.commit()

def find_notebook_by_id(notebook_id):
    return session.query(Notebook).filter_by(id=notebook_id).first()

def modify_notebook_position(notebook_id, index):
    to_modify_notebook = find_notebook_by_id(notebook_id)
    user_id = to_modify_notebook.user_id
    if to_modify_notebook.index > index:
        shift_notebooks(user_id, index, to_modify_notebook.index)
        to_modify_notebook.index = index
    elif to_modify_notebook.index < index:    
        shift_notebooks(user_id, to_modify_notebook.index + 1, index + 1, True)
        to_modify_notebook.index = index
    session.commit()    

def get_all_notebooks_by_user_id(user_id):
    return session.query(Notebook).filter_by(user_id=user_id).all()

def change_active_notebook(user_id, notebook_id):
    user = session.query(User).filter_by(id=user_id).first()
    user.active_notebook_id = notebook_id
    session.commit()
