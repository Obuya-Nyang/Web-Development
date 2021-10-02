import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = 'mysql+pymysql://root:obuyanyang@127.0.0.1:3306/fastap'
engine = create_engine(database_url, echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()