from sqlalchemy import Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
