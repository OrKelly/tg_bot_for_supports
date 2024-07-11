import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(url=DATABASE_URL)

session_maker = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)
