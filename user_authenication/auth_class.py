from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    frist_name:str
    last_name:str
    email_sddress:str
    password:str
    user_role:Optional[str]
    disabled:Optional[bool] = False

class LoginRequest(BaseModel):
    email_address:str
    password:str

class AccessToken(BaseModel):
    email_address:str
    access_token:str
    token_type:str