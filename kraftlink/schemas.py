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
    id:int
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class Consumer(BaseModel):
    user: User
    model_config = ConfigDict(from_attributes=True)

class Manufacturer(BaseModel):
    user: User
    model_config = ConfigDict(from_attributes=True)

class Installer(BaseModel):
    user: User
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token : str
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