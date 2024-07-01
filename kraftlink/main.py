from datetime import timezone
import shutil
from fastapi import FastAPI,Depends,HTTPException,status, UploadFile, File
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
UPLOAD_DIRECTORY = "./uploads"  # Directory to store uploaded images
# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
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
@app.get("/get_account", response_model=AccountResponse)
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
@app.post("/create_share/", response_model=ShareResponse, status_code=status.HTTP_201_CREATED)
async def create_share(share: ShareCreate, db: Session = Depends(get_db)):
    db_share = models.SharesTable(
        amount_nok=share.amount_nok,
        account_id=share.account_id,
        project_id=share.project_id,
        percentage_share=share.percentage_share,
        profit_margin=share.profit_margin,
        register_time=datetime.now(timezone.utc)
    )
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share
# delete shares
@app.delete("/shares/{share_id}", response_model=ShareResponse)
async def delete_share(share_id: int, db: Session = Depends(get_db)):
    db_share = db.query(models.SharesTable).filter(models.SharesTable.id == share_id).first()
    if db_share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    db.delete(db_share)
    db.commit()
    return db_share
# update shares
@app.put("/shares/{share_id}", response_model=ShareResponse)
async def update_share(share_id: int, share: ShareUpdate, db: Session = Depends(get_db)):
    db_share = db.query(models.SharesTable).filter(models.SharesTable.id == share_id).first()
    if db_share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    update_data = share.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_share, key, value)
    db.commit()
    db.refresh(db_share)
    return db_share
# get shares
@app.get("/shares/{share_id}", response_model=ShareResponse)
async def read_share(share_id: int, db: Session = Depends(get_db)):
    share = db.query(models.SharesTable).filter(models.SharesTable.id == share_id).first()
    if share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    return share

# PRODUCT
# create product
@app.post("/create_product/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.ProductsTable(
        manufacturer_id=product.manufacturer_id,
        project_id=product.project_id,
        name=product.name,
        category_id=product.category_id,
        register_time=datetime.now(timezone.utc)
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# delete product
@app.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductsTable).filter(models.ProductsTable.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product

# update product
@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.ProductsTable).filter(models.ProductsTable.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# Read a product by ID
@app.get("/products/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.ProductsTable).filter(models.ProductsTable.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

#PROJECT
# create project
@app.post("/create_project/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.ProjectsTable(
        installer_id=project.installer_id,
        location=project.location,
        name=project.name,
        type_of_facility=project.type_of_facility,
        capacity=project.capacity,
        realtime_electricity_generation=project.realtime_electricity_generation,
        number_of_shares=project.number_of_shares,
        cost_nok=project.cost_nok,
        money_required=project.money_required,
        money_spent=project.money_spent,
        money_left=project.money_left,
        electricity_generation_prediction=project.electricity_generation_prediction,
        manufacturer_status=project.manufacturer_status,
        installer_status=project.installer_status,
        funded_status=project.funded_status,
        register_time=datetime.now(timezone.utc)
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# delete project
@app.delete("/project/{project_id}", response_model=ProjectResponse)
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.ProjectsTable).filter(models.ProjectsTable.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return db_project

# update project
@app.put("/project/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(models.ProjectsTable).filter(models.ProjectsTable.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

# get project
@app.get("/projects/{project_id}", response_model=ProjectResponse)
async def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.ProjectsTable).filter(models.ProjectsTable.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

#category
# create category
@app.post("/create_category/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.CategoriesTable(
        name=category.name,
        register_time=datetime.now(timezone.utc)
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# delete category
@app.delete("/categories/{category_id}", response_model=CategoryResponse)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.CategoriesTable).filter(models.CategoriesTable.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category

# update category
@app.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(models.CategoriesTable).filter(models.CategoriesTable.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

# get category
@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.CategoriesTable).filter(models.CategoriesTable.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

#Images
# create images
@app.post("/post_image/", response_model=ImageResponse, status_code=201)
async def create_image(
    category_id: int,
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create image metadata
    db_image = models.ImagesTable(
        category_id=category_id,
        product_id=product_id,
        file_path=file_path,
        register_time=datetime.now(timezone.utc)
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

# delete images
@app.delete("/images/{image_id}", response_model=ImageResponse)
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(models.ImagesTable).filter(models.ImagesTable.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    # Delete the file from the filesystem
    if os.path.exists(db_image.file_path):
        os.remove(db_image.file_path)
    db.delete(db_image)
    db.commit()
    return db_image

# update images
@app.put("/images/{image_id}", response_model=ImageResponse)
async def update_image(image_id: int, image: ImageUpdate, db: Session = Depends(get_db)):
    db_image = db.query(models.ImagesTable).filter(models.ImagesTable.id == image_id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    update_data = image.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_image, key, value)
    db.commit()
    db.refresh(db_image)
    return db_image
# get images
@app.get("/images/{image_id}", response_model=ImageResponse)
async def read_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(models.ImagesTable).filter(models.ImagesTable.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image










