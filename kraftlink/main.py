from fastapi import FastAPI,Depends,HTTPException,status
from .schemas import *
from .utils import *
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, models, database,utils
from .database import engine
db = {
    'tim': {
        'username' : 'tim',
        'fullname' : 'tim cook',
        'email':'tim@gmail.com',
        'user_type': 'consumer',
        'hashed_password' : '$2b$12$phkYFHvw8oVTXrMyS4FdEeW32TJetD.1402kak.GwgM6Xgzjmyh06',
        'disabled' : False,
    }
}

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
#################  USER REGISTRATION


@app.post("/register", response_model=schemas.User)
async def register_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_user = crud.create_user(db=db, user_data=user_data)
    
    # Check user type and create appropriate record
    if user_data.user_type == "manufacturer":
        return crud.create_manufacturer(db, user_id=new_user.id)
    elif user_data.user_type == "installer":
        return crud.create_installer(db, user_id=new_user.id)
    else:  # Default to consumer
        return crud.create_consumer(db, user_id=new_user.id)





####################### USER LOGIN and AUTHENTICATION
@app.post("/token",response_model=Token)
async def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail= "Incorrect username or password",headers={"WWW-Authenticate":"Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub": user.username},expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
    

@app.get("/users/me/",response_model= User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id":1, "owner": current_user}]







