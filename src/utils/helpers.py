from fastapi import Request, HTTPException, status, Depends
from src.utils.settings import settings
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from src.user.models import UserModel
import jwt
from src.utils.db import get_db





 




def is_authenticated(request:Request, db:Session= Depends(get_db)):
   try:
           token = request.headers.get ("authorization")
           if not token:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
    
           token = token.split(" ") [-1]

           data = jwt. decode(token, settings.SECRET_KEY, settings.ALGORITHM)
           user_id = data.get("_id")
           User = db. query (UserModel). filter(UserModel.id == user_id).first()
           if not User:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")
           return User

   except InvalidTokenError: 
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized.")