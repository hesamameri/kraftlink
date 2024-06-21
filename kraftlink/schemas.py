from pydantic import BaseModel,EmailStr




class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username:str
    fullname: str | None = None
    email : EmailStr | None = None
    user_type: str | None = None
    disabled : bool | None = None


class UserInDB(User):
    hashed_password : str