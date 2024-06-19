# crud.py
from sqlalchemy.orm import Session
from . import models, schemas, utils

def get_user(db: Session, username: str):
    return db.execute(models.users.select().where(models.users.c.username == username)).fetchone()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    db.execute(models.users.insert().values(username=user.username, hashed_password=hashed_password))
    db.commit()
