
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas, utils

############### User Registration 
def create_user(db: Session, user_data: schemas.UserCreate) -> schemas.UserInDB:
    hashed_password = utils.get_password_hash(user_data.password)
    user_in_db = models.UserTable(
        username=user_data.username,
        fullname=user_data.fullname,
        email=user_data.email,
        user_type=user_data.user_type,
        disabled=user_data.disabled,
        hashed_password=hashed_password
    )
    
    if db.query(models.UserTable).filter(models.UserTable.username == user_in_db.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)
    
    return schemas.UserInDB.from_orm(user_in_db)

def create_consumer(db: Session, user_id: int) -> schemas.User:
    consumer = models.ConsumerTable(user_id=user_id)
    db.add(consumer)
    db.commit()
    db.refresh(consumer)
    return schemas.User.from_orm(consumer.user)

def create_manufacturer(db: Session, user_id: int) -> schemas.User:
    manufacturer = models.ManufacturerTable(user_id=user_id)
    db.add(manufacturer)
    db.commit()
    db.refresh(manufacturer)
    return schemas.User.from_orm(manufacturer.user)

def create_installer(db: Session, user_id: int) -> schemas.User:
    installer = models.InstallerTable(user_id=user_id)
    db.add(installer)
    db.commit()
    db.refresh(installer)
    return schemas.User.from_orm(installer.user)

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.UserTable).offset(skip).limit(limit).all()