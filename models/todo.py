from sqlalchemy import Column, Integer, String #type: ignore
from sqlalchemy.ext.declarative import declarative_base #type: ignore

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)