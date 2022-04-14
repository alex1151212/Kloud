from json import load
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form,APIRouter
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import Any, Dict, List
import os
from dotenv import load_dotenv,find_dotenv ,dotenv_values

credentials = dotenv_values('.env')
# credentials = {
#     "EMAIL":os.getenv('EMAIL'),
#     "PASS" : os.getenv('PASS')
#     }

class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = credentials['EMAIL'],
    MAIL_PASSWORD = credentials['PASS'],
    MAIL_FROM = credentials['EMAIL'],
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app = FastAPI()

@app.get('/')
async def root():
    return "root"
# http://localhost:8000/verification/?token{token}

# @app.post("/email")
# async def simple_send(email: EmailSchema):

#     message = MessageSchema(
#         subject="Verification Email Test",
#         recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
#         body=html,
#         subtype="html"
#         )

#     fm = FastMail(conf)
#     await fm.send_message(message)
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})

@app.post("/email")
async def simple_send(request:Request,email: EmailSchema,url:str) -> JSONResponse:

    html = f"""
 Click the Link to Verify your account {url}
"""

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})      

