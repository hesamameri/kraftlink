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
    account_id: int
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
    user_id: int
    name: str
    surname: str
    company_name: str
    balance_nok: float
    register_time: datetime
    bank_card_number: str
    bank: str
    cvv: str
    model_config = ConfigDict(from_attributes=True)

class Share(BaseModel):
    amount_nok: float
    account_id: int
    project_id: int
    percentage_share: float
    profit_margin: float
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)

class Project(BaseModel):
    installer_id: int
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
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)

class Product(BaseModel):
    manufacturer_id: int
    project_id: int
    name: str
    category_id: int
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)

class Category(BaseModel):
    name: str
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)

class Image(BaseModel):
    category_id: int
    product_id: int
    register_time: datetime
    model_config = ConfigDict(from_attributes=True)
