from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     username = Column(String, unique=True)
#     password = Column(String)

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    # owner = Column(Integer, ForeignKey("users.id"))