from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    frist_name:str
    last_name:str
    email_sddress:str
    password:str
    user_role:Optional[str]
    disabled:Optional[bool] = False

class EditUser(BaseModel):
    id:str
    frist_name:str
    last_name:str
    username:str
    password:str
    role:str
    is_active:bool
    created_at:str

class LoginRequest(BaseModel):
    email_address:str
    password:str

class AccessToken(BaseModel):
    frist_name:str
    last_name:str
    access_token:str
    token_type:str