from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema, UserResponnseSchema,  LoginSchema
from src.user import controller



user_routes =APIRouter(prefix="/user")

#user first time registration route
@user_routes.post("/register",response_model=UserResponnseSchema, status_code = status.HTTP_201_CREATED)
async def register_user(body: UserSchema,bg_task:BackgroundTasks, db: Session = Depends(get_db)):

    return await controller.register(body, db, bg_task)  

#user login route
@user_routes.post("/login", status_code= status.HTTP_200_OK)
def login(body: LoginSchema,db: Session = Depends(get_db)): 
    return controller.login_user(body,db)

#token send

@user_routes.get("/is_auth",response_model=UserResponnseSchema, status_code= status.HTTP_200_OK)
def is_auth(request:Request,db: Session = Depends(get_db)):
    return controller.is_authenticated(request,db)
 
    
