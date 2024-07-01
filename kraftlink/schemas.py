from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[str] = None
    disabled: Optional[bool] = None

class UserCreate(User):
    password: str

class UserInDB(User):
    id: int
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[str] = None
    disabled: Optional[bool] = None

class Consumer(BaseModel):
    user: User
    address: Optional[str] = None
    phone_number: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class Manufacturer(BaseModel):
    user_id: int
    comp_name: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    account_id: int|Optional[str] = None
    comp_register_number: Optional[str] = None
    company_size: Optional[str] = None
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)

class Installer(BaseModel):
    user_id: int
    comp_name: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    account_id: Optional[int] = None
    comp_register_number: Optional[str] = None
    company_size: Optional[str] = None
    register_time: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# New models
class Account(BaseModel):
    id: int
    user_id: int
    name: str
    surname: str
    company_name: str
    balance_nok: float
    register_time: datetime
    bank_card_number: str
    bank: str
    cvv: str

    class Config:
        orm_mode = True
class AccountCreate(BaseModel):
    name: str
    surname: str
    company_name: str
    balance_nok: float
    register_time: datetime
    bank_card_number: str
    bank: str
    cvv: str

    class Config:
        orm_mode = True
        from_attributes = True

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    company_name: Optional[str] = None
    balance_nok: Optional[float] = None
    bank_card_number: Optional[str] = None
    bank: Optional[str] = None
    cvv: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
class AccountResponse(BaseModel):
    name: str
    surname: str
    company_name: str
    balance_nok: float
    register_time: datetime
    bank_card_number: str
    bank: str
    cvv: str

    class Config:
        orm_mode = True
        from_attributes = True
class Share(BaseModel):
    amount_nok: float
    account_id: int
    project_id: int
    percentage_share: float
    profit_margin: float
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)
class ShareCreate(Share):
    pass

class ShareUpdate(BaseModel):
    amount_nok: Optional[float] = None
    account_id: Optional[int] = None
    project_id: Optional[int] = None
    percentage_share: Optional[float] = None
    profit_margin: Optional[float] = None

class ShareResponse(Share):
    id: int
    register_time: datetime

    class Config:
        orm_mode = True
        from_attributes = True
class Project(BaseModel):
    location: str
    name: str
    type_of_facility: str
    capacity: float
    realtime_electricity_generation: float
    number_of_shares: int
    cost_nok: float
    money_required: float
    money_spent: float
    money_left: float
    electricity_generation_prediction: str
    manufacturer_status: str
    installer_status: str
    funded_status: str

class ProjectCreate(Project):
    installer_id: Optional[int] = None

class ProjectUpdate(BaseModel):
    installer_id: Optional[int] = None
    location: Optional[str] = None
    name: Optional[str] = None
    type_of_facility: Optional[str] = None
    capacity: Optional[float] = None
    realtime_electricity_generation: Optional[float] = None
    number_of_shares: Optional[int] = None
    cost_nok: Optional[float] = None
    money_required: Optional[float] = None
    money_spent: Optional[float] = None
    money_left: Optional[float] = None
    electricity_generation_prediction: Optional[str] = None
    manufacturer_status: Optional[str] = None
    installer_status: Optional[str] = None
    funded_status: Optional[str] = None

class ProjectResponse(Project):
    id: int
    installer_id: Optional[int]
    register_time: datetime

    class Config:
        orm_mode = True
        from_attributes = True



class Product(BaseModel):
    manufacturer_id: int
    project_id: int
    name: str
    category_id: int
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)
class ProductCreate(Product):
    pass
class ProductUpdate(BaseModel):
    manufacturer_id: Optional[int] = None
    project_id: Optional[int] = None
    name: Optional[str] = None
    category_id: Optional[int] = None
class ProductResponse(Product):
    id: int
    register_time: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class Category(BaseModel):
    name: str

class CategoryCreate(Category):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(Category):
    id: int
    register_time: datetime

    class Config:
        from_attributes = True


class Image(BaseModel):
    category_id: int
    product_id: int

class ImageCreate(Image):
    pass
class ImageUpdate(BaseModel):
    category_id: Optional[int] = None
    product_id: Optional[int] = None

class ImageResponse(Image):
    id: int
    file_path: str
    register_time: datetime

    class Config:
        from_attributes = True  # Correctly use from_attributes for Pydantic v2
