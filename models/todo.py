from sqlalchemy import Column, Integer, String,ForeignKey#type: ignore
from sqlalchemy.ext.declarative import declarative_base #type: ignore

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
class Api_key(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True, index=True)     
    key = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
   

    