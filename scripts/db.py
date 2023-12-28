from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
import os

SERVER = os.environ.get('SERVER')
DATABASE = os.environ.get('DATABASE')
LOGIN = os.environ.get('LOGIN')
PASSWORD = os.environ.get('PASSWORD')

engine = create_engine(f'mssql+pyodbc://{SERVER}/{DATABASE}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')


Base = declarative_base()

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    file_size = Column(Float)
    table_name = Column(String)
    status = Column(String)
    start_date = Column(DateTime)
    duration = Column(Float)

Base.metadata.create_all(bind=engine)

