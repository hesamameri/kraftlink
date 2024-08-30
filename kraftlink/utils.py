from jose import JWTError
from jose import jwt
from passlib.context import CryptContext
from .schemas import *
from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas, utils
from .database import get_db

load_dotenv()  
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto" )
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")






################### User Login and Authentication

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(models.UserTable).filter(models.UserTable.username == username).first()
def authenticate_user(db,username:str,password:str):
    user = get_user(db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

def create_access_token(data:dict,expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta :
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token:str = Depends(oauth_2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user(db,username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code = 400, detail= "inactive User")
    return current_user


######################