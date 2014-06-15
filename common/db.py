import json
import sqlalchemy as sc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = sc.create_engine(config.DATABASE_URI, echo=config.ECHO)
session = sessionmaker(bind=engine)()
Base = declarative_base(engine)

def init_db():
  Base.metadata.create_all()
