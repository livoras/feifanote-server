# -*- coding: utf-8 -*-
from models.notebook import Notebook
from models.page import Page
from common.db import session
from sys import maxint

def add_new_page(notebook_id, index):
    shift_notebooks(notebook_id, index, maxint)
    page = Page(**dict(notebook_id=notebook_id, index=index))
    session.add(page)
    session.commit()
    return page

def shift_notebooks(notebook_id, _from, to, back=False):
    to_shift_pages = session.query(Page).filter(
        Page.notebook_id==notebook_id,
        Page.index>=_from,
        Page.index<to)
    for page in to_shift_pages:
        if back:
            page.index -= 1
        else:    
            page.index += 1
    session.commit()
