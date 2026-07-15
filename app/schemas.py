from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)