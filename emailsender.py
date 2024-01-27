from typing import List

from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME="amritanandsingh0305@gmail.com",
    MAIL_PASSWORD="evevhxmkcotmkikr",  # Use the App Password generated for your Google account
    MAIL_FROM="amritanandsingh0305@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",  # Use the SMTP server for Gmail
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

app = FastAPI()


html = """
<p>Thanks for using Fastapi-mail</p> 
"""


@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})   