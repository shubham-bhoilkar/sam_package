from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index= True)
    username = Column(String, unique= True, index= True)
    hashed_password = Column(String)

'''
from schemas import UserInDB

users_db ={
    "john":{"usernme":"john",
            "hashed_password":"$2b$12$wUIy1T9KaPI9T9K/e9GMeOt1ZmY/Z8NNK3qpuEJ.fEzABa1PpqEFi"}
    }

def get_user(username: str)-> UserInDB:
    user= users_db.get(username)
    if user:
        return UserInDB(**user)
'''    