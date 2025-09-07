from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: str
    password:str
    role:str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_name: str
    email: str
    role: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email:str
    user_name: Optional[str] = None
    password: str

class UserLogout(BaseModel):
    token:str

class ChangePassword(BaseModel):
    token:str
    current_password:str 
    new_password:str 

class Token(BaseModel):
    access_token: str
    token_type: str
    

##### Settings schema

class SettingBase(BaseModel):
    type: str
    group: str
    key: str
    value: str


class SettingCreate(SettingBase):
    pass


class SettingUpdate(BaseModel):
    type: Optional[str] = None
    group: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None


class SettingOut(SettingBase):
    id: int

    class Config:
        orm_mode = True


class SettingsList(BaseModel):
    settings: List[SettingOut]