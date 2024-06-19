# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from kraftlink import models, schemas, crud, dependencies, auth, utils

app = FastAPI()

@app.on_event("startup")
async def startup():
    await dependencies.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await dependencies.database.disconnect()

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=dict)
def login_for_access_token(db: Session = Depends(dependencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user(db, username=form_data.username)
    if not user or not utils.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/test-db-connection")
async def test_db_connection(db: Session = Depends(dependencies.get_db)):
    try:
        result = db.execute("SELECT 1")
        return {"status": "success", "result": result.fetchone()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
