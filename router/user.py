from os import access
import re
from typing import List
from fastapi import (
    APIRouter ,
    Depends,
    Response, 
    status ,
    HTTPException,
    Request,
    Cookie
)
from regex import F

#Database 
from database import get_db
from sqlalchemy.orm import Session
from schemas import *
import models

#Security
import JWTtoken
from hash import Hash
from fastapi.security import OAuth2PasswordRequestForm
from oauth import get_current_user

UserApp = APIRouter(
    
)


@UserApp.post('/login',tags=["APIs",'User'])
async def login(response:Response,userInput=Depends(OAuth2PasswordRequestForm),db:Session=Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email==userInput.username).first()
    if not user:
        raise HTTPException(
            status_code = 400 , 
            detail = f"Doesn't exist this User!"
            )
    if not Hash.verify(user.password,userInput.password):
        raise HTTPException(
            status_code= 401,
            detail = f"Invalid username or password!"
        )
    roles = []
    for role in roles:
        roles.append(role.name)
    accessToken = JWTtoken.create_access_token(
        data={
            "username":user.email,
            "roles":roles,
        }
    )
    response.set_cookie(key="Authorization",value=accessToken,httponly=True)
    return {
        "access_token":accessToken ,
        "token_type":"bearer",
        "username":user.email,
        "roles":roles,
        } 

@UserApp.post('/register',tags=["APIs",'User'])
async def createUser(userInput:Register,db:Session=Depends(get_db)):
    new_user = models.User(
        name=userInput.username,
        password=Hash.bcrypt(userInput.password),
        email=userInput.email,
        birthday=userInput.birthday,
        school_id = userInput.schoolID ,
        school_grade = userInput.schoolGrade,
    )

    user = db.query(models.User).filter(models.User.email==userInput.email).first()
    if user :
        raise HTTPException(409,detail=f'This User is exist already')

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@UserApp.put('/user',tags=['APIs','User'])
async def updateUser(userInput:UserEdit,user=Depends(get_current_user),db:Session=Depends(get_db)):
    userInfo = {
        'name':userInput.username,
        'password':Hash.bcrypt(userInput.password),
        'email':userInput.email,
        'birthday':userInput.birthday,
        'school_id' : userInput.schoolID ,
        'school_grade' : userInput.schoolGrade,
    }
    U = db.query(models.User).filter(models.User.email==user)
    U.update(userInfo)
    db.commit()
    
    return "Update Successfully!"




@UserApp.get('/user',tags=['DevAPIs','User'])
async def getUserAll(db:Session=Depends(get_db)):
    user = db.query(models.User).all()

    return user

@UserApp.get('/user/{userEmail}',tags=["DevAPIs",'User'])
async def getUserByEmail(userEmail:str,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==userEmail).first()
    
    if not user:
        raise HTTPException(404,detail=f"This User is not exist")
    
    return user



@UserApp.get('/role/{username}',tags=['DevAPIs','Role'])
async def getRoles(username:str,db:Session=Depends(get_db)):

     user = db.query(models.User).filter(models.User.email==username).first()

     return user.roles

    
@UserApp.get('/role',tags=['DevAPIs','Role'])
async def getRolesAll(db:Session=Depends(get_db)):

    roles = db.query(models.Role).all()

    if not db.query(models.Role).first():
        raise HTTPException(404,detail='Role Not Found')

    return roles

@UserApp.post('/role',tags=['DevAPIs','Role'])
async def createRole(newrole:NewRole,db:Session=Depends(get_db)):
    
    newRole = models.Role(
        name=newrole.name
    )

    role = db.query(models.Role).filter(models.Role.name==newrole.name).first()
    if role:
       raise HTTPException(409) 
    
    db.add(newRole)
    db.commit()
    db.refresh(newRole)

    return newRole


@UserApp.delete('/role/{name}',tags=['DevAPIs','Role'])
async def deleteRole(name:str,db:Session=Depends(get_db)):

    role = db.query(models.Role).filter(models.Role.name==name)
    if not role.first():
        raise HTTPException(404,detail="Role Not Found")

    role.delete()
    db.commit()

    return "Delete Role Successfully"

@UserApp.put('/role',tags=['DevAPIs','Role'])
async def addRoleToUser(roles:List[str],user=Depends(get_current_user),db:Session=Depends(get_db)):
    
    test =[]
    for role in roles:
        R = db.query(models.Role).filter(models.Role.name==role).first()

        if not R :
            raise HTTPException(404,detail=f'Role with name {role} is not found')

        U = db.query(models.User).filter(models.User.email==user).first()
        if U.roles.count(role) >=1:
            raise HTTPException(409)
        # test.append(R)
    
        U.roles.append(R)
    
    db.commit()
    # U = db.query(models.User).filter(models.User.email==user).first()
    return "Role Add Success!"
    # return test
    