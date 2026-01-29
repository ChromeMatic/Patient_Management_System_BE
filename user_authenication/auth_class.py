from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class user_credentials(BaseModel):
    username:str
    password:str