from fastapi import FastAPI
from models import User , Expense , Balance , Participant
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from typing import List
from fastapi import HTTPException

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

expenses_data: List[Expense] = [
    Expense(
        expenseId="e1",
        userid="user1",
        amount=1000.0,
        type="exact",
        expenseName="Electricity Bill",
        notes="Paid for electricity",
        participants=[
            {"userid": "user2", "share": 500.0},
            {"userid": "user3", "share": 200.0},
            {"userid": "user4", "share": 250.0}
        ]
    ),
    Expense(
        expenseId="e2",
        userid="user2",
        amount=1200.0,
        type="percent",
        expenseName="Dinner",
        notes="Shared dinner expenses",
        participants=[
            {"userid": "user1", "share": 40.0},
            {"userid": "user4", "share": 30.0},
            {"userid": "user3", "share": 30.0}
        ]
    ),

]

balance_data: List[Participant] = [
    Balance(
        userid="user1",
        BalancesForEveryone=[
            {"userid": "user2", "share": 500.0},
            {"userid": "user3", "share": 200.0},
            {"userid": "user4", "share": 250.0}
        ]
    ),
    Balance(
        userid="user2",
        BalancesForEveryone=[
            {"userid": "user1", "share": 40.0},
            {"userid": "user4", "share": 30.0},
            {"userid": "user3", "share": 30.0}
        ]
    )
]

app = FastAPI()

@app.get("/")
def read_root():
    #sendmail("amritanandsingh999@gmail.com", "Test Subject", "Text body", "<p>HTML body</p>")
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

@app.get('/api/expence/all')
def getAllExpence():
    return expenses_data,balance_data
    
@app.post('/api/expence/add')
async def add_expense(expense: Expense):
    try:
        type_of_expense = {"percent", "exact", "equal"}
    
        total_amount = sum(participant.share for participant in expense.participants)

        #print(expense.type.lower())

        if expense.type.lower() not in type_of_expense:
            return {"message": "Error in expense type"}

        if expense.type.lower() == "percent" and total_amount != 100 :
            return {"message": "Total share percent does not match the expense amount"}
        elif total_amount != expense.amount:
            return {"message": "Total share amount does not match the expense amount"}
        
        expenses_data.append(expense)
        
            
        await mailToParticipants(expense)
        
        for balance in balance_data:
            if balance.userid == expense.userid:
                add_expense_helper(balance, expense.participants)
                return {"message": "Successfully added Expense and updated existing Expense"}

        balance_data.append({"userid": expense.userid, "BalancesForEveryone": expense.participants})

        return {"message": "Successfully added Expense"}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}

def add_expense_helper(balance, expense_participants):
    dic1 = {participant.userid: participant.share for participant in balance.BalancesForEveryone}

    for participant in expense_participants:
        userid = participant.userid
        share = participant.share

        if userid is not None and share is not None:
            dic1[userid] = dic1.get(userid, 0) + share

    balance.BalancesForEveryone = [{"userid": userid, "share": share} for userid, share in dic1.items()]

@app.get('/api/expence/user')
async def getUserExpence(userid:str):
    data = []
    userid = 'user1'
    for i in expenses_data:
        if i.userid == userid:
            data.append(i)
    return data

@app.get('/api/expence/user/carryoff/')  # get all the users where there is a non-zero balance
async def getUserExpence(userid:str):
    data = []
    userid = 'user1'
    for i in balance_data:
        if i.userid == userid:
            data = i.BalancesForEveryone
    return data


#------------------mail setup --------------------------------
class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME="amritanandsingh0305@gmail.com",
    MAIL_PASSWORD="evevhxmkcotmkikr",  #  Password 
    MAIL_FROM="amritanandsingh0305@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",  # Use the SMTP server for Gmail
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

html = """
<p>Thanks for using Splitwise-mail</p> 
"""

html1 = """
you have been added to an expense
"""

@app.post('/api/email')
async def simple_send(email: EmailSchema) -> JSONResponse:
    try:
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=email.dict().get("email"),
            body=html,
            subtype=MessageType.html)

        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def sendmail(email, subject, body, html_content):

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

async def mailToParticipants(expense):
    dic = {}
    for i in expense.participants:
        dic[i.userid] = i.share
    for i in db:
        if dic.get(i.userid) != None:
            await sendmail(i.email , "You have added to an expence for { dic.get(i.userid) }" , expense.name )




