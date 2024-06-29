
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas, utils
import logging
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
    # print(f"Created User: {user_in_db.id}, Type: {user_data.user_type}") 
    if db.query(models.UserTable).filter(models.UserTable.username == user_in_db.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)
    
    return schemas.UserInDB.model_validate(user_in_db)

def create_consumer(db: Session, user_id: int) -> schemas.UserInDB:
    try:
        consumer = models.ConsumerTable(user_id=user_id)
        db.add(consumer)
        db.commit()
        db.refresh(consumer)
        return schemas.UserInDB.model_validate(consumer.user)
    except Exception as e:
        logging.error(f"Error in create_consumer: {e}")
        raise HTTPException(status_code=500, detail="Failed to create consumer record")

def create_manufacturer(db: Session, user_id: int) -> schemas.UserInDB:
    try:
        manufacturer = models.ManufacturerTable(user_id=user_id)
        db.add(manufacturer)
        db.commit()
        db.refresh(manufacturer)
        return schemas.UserInDB.model_validate(manufacturer.user)
    except Exception as e:
        logging.error(f"Error in create_manufacturer: {e}")
        raise HTTPException(status_code=500, detail="Failed to create manufacturer record")

def create_installer(db: Session, user_id: int) -> schemas.UserInDB:
    try:
        installer = models.InstallerTable(user_id=user_id)
        db.add(installer)
        db.commit()
        db.refresh(installer)
        return schemas.UserInDB.model_validate(installer.user)
    except Exception as e:
        logging.error(f"Error in create_installer: {e}")
        raise HTTPException(status_code=500, detail="Failed to create installer record")

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.UserTable).offset(skip).limit(limit).all()




# show all the Manufacturers, Installers , Consumers,Products,Shares,Projects,CAtegories,Images

# register manufacturer Data -- > Complete their data 
# register Installer Data -- > Complete their data
# create Account based on the user and manufacturer data
# delete USer, Manufacturer, Installer , account
# update User,Manufacturer, Installer , account DATA

# create, delete, update SHARE
# create ,delete,update PRODUCT
# create,register ,delete,update PROJECT
# CRUD CATEGORY and IMAGES


# Add ROLE TO EACH USER UPGRADE USERS , DOWNGRADE USERS










