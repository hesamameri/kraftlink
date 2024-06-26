from pydantic import BaseModel,EmailStr

from pydantic import BaseModel, EmailStr
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
    hashed_password: str

class Consumer(BaseModel):
    user: User

class Manufacturer(BaseModel):
    user: User

class Installer(BaseModel):
    user: User

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None




