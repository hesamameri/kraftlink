from fastapi import FastAPI,Depends,HTTPException,status
from .schemas import *
from .utils import *
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, models, database,utils
from .database import engine,get_db
from fastapi.concurrency import run_in_threadpool
import logging

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
#################  USER REGISTRATION


@app.post("/register", response_model=schemas.User)
async def register_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Create a new user in a thread pool
    try:
        new_user = await run_in_threadpool(crud.create_user, db=db, user_data=user_data)
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user")

    # Check user type and create appropriate record in a thread pool
    try:
        if user_data.user_type == "manufacturer":
            result = await run_in_threadpool(crud.create_manufacturer, db, user_id=new_user.id)
        elif user_data.user_type == "installer":
            result = await run_in_threadpool(crud.create_installer, db, user_id=new_user.id)
        else:  # Default to consumer
            logging.info("Defaulting to consumer type")
            result = await run_in_threadpool(crud.create_consumer, db, user_id=new_user.id)
        logging.info(f"Successfully created {user_data.user_type} record for user ID {new_user.id}")
        return result
    except Exception as e:
        logging.error(f"Error creating {user_data.user_type} record: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create {user_data.user_type} record")






####################### USER LOGIN and AUTHENTICATION
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))    
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
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







