from fastapi import FastAPI
from models import User
from typing import List

db: List[User] =[
    User(
        userid="user1",
        name="amrit",
        email="amritanandsingh999@gmail.com",
        phonenumber="1111111111"
    ),
    User(
        userid="user2",
        name="prince",
        email="princeraj00580@gmail.com",
        phonenumber="2222222222"
    ),
    User(
        userid="user3",
        name="aviraj",
        email="amritanandsingh0305@gmail.com",
        phonenumber="3333333333"
    ),
    User(
        userid="user4",
        name="vishal",
        email="vishalkumarsingh999@gmail.com",
        phonenumber="4444444444"
    ),
]


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/api/user/all')
def getAllUser():
    return db

@app.post('/api/user/add')
def createUser(user:User):
    db.append(user)
    return {
        "message":"user Added into DB"
    }

