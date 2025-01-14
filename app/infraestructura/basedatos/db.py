import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = 'inventarios.db'
base_dir = os.path.dirname(os.path.realpath(__file__))
databaseUrl = f'sqlite:///{os.path.join(base_dir, sqliteName)}'

engine = create_engine(databaseUrl, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    print('HERE')
    db = Session()
    try:
        yield db
        print('HERE 2')
    finally:
        db.close()
