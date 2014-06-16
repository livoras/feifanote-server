from models.user import User
from models.notebook import Notebook
from models.page import Page
from common import db
from app import app

session = db.session

def setup(self):
    user = User(**dict(
        email="iammfw@163.com", 
        username="jerry", 
        password="123456", 
        active_notebook_id=1
    ))

    notebook1 = Notebook(**dict(
        user_id=1,
        active_page_id=1,
        name="notebook1",
        index=1
    ))

    notebook2 = Notebook(**dict(
        user_id=1,
        active_page_id=1,
        name="notebook1",
        index=2
    ))

    page1 = Page(**dict(
        notebook_id=1,
        content="This is my first love",
        index=1
    ))

    page2 = Page(**dict(
        notebook_id=1,
        content="This is my first love",
        index=2
    ))

    session.add_all([user, notebook1, notebook2, page1, page2])
    session.commit()

def test_db():
    u = session.query(User).filter_by(id=1).first()
    assert u.username == 'jerry'
    assert len(u.notebooks) == 2

    notebooks = session.query(Notebook).all()
    assert len(notebooks) == 2

    notebook1 = session.query(Notebook).first()
    assert len(notebook1.pages) == 2

