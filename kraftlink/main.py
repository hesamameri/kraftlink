from datetime import timezone
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
from typing import Union


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
#######################################  ADMIN DATA DISPLAY OF ALL DATABASE OBJECTS
@app.get('/users', response_model=List[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.UserTable).all()
    return users
@app.get('/consumers', response_model=List[schemas.Consumer])
async def get_users(db: Session = Depends(get_db)):
    consumers = db.query(models.ConsumerTable).all()
    return consumers
@app.get('/installers', response_model=List[schemas.Installer])
async def get_users(db: Session = Depends(get_db)):
    installers = db.query(models.InstallerTable).all()
    return installers
@app.get('/manufacturers', response_model=List[schemas.Manufacturer])
async def get_users(db: Session = Depends(get_db)):
    manufacturers = db.query(models.ManufacturerTable).all()
    return manufacturers

@app.get('/all/projects', response_model=List[schemas.Project])
async def get_users(db: Session = Depends(get_db)):
    projects = db.query(models.ProjectsTable).all()
    return projects

@app.get('/all/products', response_model=List[schemas.Product])
async def get_users(db: Session = Depends(get_db)):
    products = db.query(models.ProductsTable).all()
    return products
@app.get('/all/shares', response_model=List[schemas.Share])
async def get_users(db: Session = Depends(get_db)):
    shares = db.query(models.SharesTable).all()
    return shares
@app.get('/all/accounts', response_model=List[schemas.Account])
async def get_users(db: Session = Depends(get_db)):
    accounts = db.query(models.AccountsTable).all()
    return accounts
@app.get('/all/categories', response_model=List[schemas.Category])
async def get_users(db: Session = Depends(get_db)):
    categories = db.query(models.CategoriesTable).all()
    return categories
@app.get('/all/images', response_model=List[schemas.Image])
async def get_users(db: Session = Depends(get_db)):
    images = db.query(models.ImagesTable).all()
    return images

####################################  Manufacturer, INSTALLER, Consumer DATA UPDATE


@app.post("/data_fill", response_model=User)
async def update_user_data(
    data: Union[Manufacturer, Installer, Consumer], 
    db: Session = Depends(get_db), 
    current_user: models.UserTable = Depends(get_current_active_user)
):
    if current_user.user_type == 'manufacturer':
        if isinstance(data, Manufacturer):
            manufacturer = db.query(models.ManufacturerTable).filter(models.ManufacturerTable.user_id == current_user.id).first()
            if not manufacturer:
                raise HTTPException(status_code=404, detail="Manufacturer not found")
            manufacturer.comp_name = data.comp_name
            manufacturer.address = data.address
            manufacturer.zip_code = data.zip_code
            manufacturer.comp_register_number = data.comp_register_number
            manufacturer.company_size = data.company_size
        else:
            raise HTTPException(status_code=422, detail="Incorrect data type for manufacturer")
        
    elif current_user.user_type == 'installer':
        if isinstance(data, Installer):
            installer = db.query(models.InstallerTable).filter(models.InstallerTable.user_id == current_user.id).first()
            if not installer:
                raise HTTPException(status_code=404, detail="Installer not found")
            installer.comp_name = data.comp_name
            installer.address = data.address
            installer.zip_code = data.zip_code
            installer.company_reg_number = data.company_reg_number
            installer.company_size = data.company_size
        else:
            raise HTTPException(status_code=422, detail="Incorrect data type for installer")
        
    elif current_user.user_type == 'consumer':
        if isinstance(data, Consumer):
            consumer = db.query(models.ConsumerTable).filter(models.ConsumerTable.user_id == current_user.id).first()
            if not consumer:
                raise HTTPException(status_code=404, detail="Consumer not found")
            consumer.address = data.address
            consumer.phone_number = data.phone_number
        else:
            raise HTTPException(status_code=422, detail="Incorrect data type for consumer")
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")

    db.commit()
    db.refresh(current_user)
    return current_user

#################################### UPDATE USER DATA

@app.put("/update_user", response_model=User)
async def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.UserTable = Depends(get_current_active_user)
):
    user = db.query(models.UserTable).filter(models.UserTable.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.fullname is not None:
        user.fullname = user_update.fullname
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.user_type is not None:
        user.user_type = user_update.user_type
    if user_update.disabled is not None:
        user.disabled = user_update.disabled

    db.commit()
    db.refresh(user)
    return user

#################################### CRUD PRODUCTS, PROJECTS, CATEGORIES, SHARES, ACCOUNTS

# Account
# create account
@app.post("/create_account", response_model=Account)
async def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db), 
    current_user: models.UserTable = Depends(get_current_active_user)
):
    # Check if the user already has an account
    existing_account = db.query(models.AccountsTable).filter(models.AccountsTable.user_id == current_user.id).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Account already exists for this user")

    # Create a new account
    new_account = models.AccountsTable(
        user_id=current_user.id,
        name=account.name,
        surname=account.surname,
        company_name=account.company_name,
        balance_nok=account.balance_nok,
        register_time=datetime.now(timezone.utc),
        bank_card_number=account.bank_card_number,
        bank=account.bank,
        cvv=account.cvv,
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

# delete account
@app.delete("/delete_account", response_model=Account)
async def delete_account(
    db: Session = Depends(get_db),
    current_user: models.UserTable = Depends(get_current_active_user)
):
    # Check if the user has an account
    account = db.query(models.AccountsTable).filter(models.AccountsTable.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Delete the account
    db.delete(account)
    db.commit()
    return account
# update account
@app.put("/update_account", response_model=Account)
async def update_account(
    account_update: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: models.UserTable = Depends(get_current_active_user)
):
    # Check if the user has an account
    account = db.query(models.AccountsTable).filter(models.AccountsTable.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Update account fields
    update_data = account_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(account, key, value)

    db.commit()
    db.refresh(account)
    return account
# get account
@app.get("/get_account", response_model=Account)
async def get_account(
    db: Session = Depends(get_db), 
    current_user: models.UserTable = Depends(get_current_active_user)
):
    # Check if the user has an account
    account = db.query(models.AccountsTable).filter(models.AccountsTable.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return account
# SHARES
# create shares
@app.post("/create_share")
async def create_share():
    pass
# delete shares
@app.delete("/delete_share")
async def delete_share():
    pass
# update shares
@app.put("/update_share")
async def update_share():
    pass
# get shares
@app.get("/get_share")
async def get_share():
    pass

# PRODUCT
# create product
@app.post("/create_product")
async def create_product():
    pass

# delete product
@app.delete("/delete_product")
async def delete_product():
    pass

# update product
@app.put("/update_product")
async def update_product():
    pass

# get product
@app.get("/get_product")
async def get_product():
    pass

#PROJECT
# create project
@app.post("/create_project")
async def create_project():
    pass

# delete project
@app.delete("/delete_project")
async def delete_project():
    pass

# update project
@app.put("/update_project")
async def update_project():
    pass

# get project
@app.get("/get_project")
async def get_project():
    pass

#category
# create category
@app.post("/create_category")
async def create_category():
    pass

# delete category
@app.delete("/delete_category")
async def delete_category():
    pass

# update category
@app.put("/update_category")
async def update_category():
    pass

# get category
@app.get("/get_category")
async def get_category():
    pass

#Images
# create images
@app.post("/create_image")
async def create_image():
    pass

# delete images
@app.delete("/delete_image")
async def delete_image():
    pass

# update images
@app.put("/update_image")
async def update_image():
    pass
# get images
@app.get("/get_image")
async def get_image():
    pass










