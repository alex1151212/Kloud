from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class Register(BaseModel):
    username: str
    email: EmailStr
    password: str
    birthday: Optional[date] = None
    schoolID: str
    schoolGrade: str


class UserEdit(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    birthday: Optional[date] = None
    schoolID: Optional[str]
    schoolGrade: Optional[str]

class NewRole(BaseModel):
    name:str
class UserAddRole(BaseModel):
    rolename:str