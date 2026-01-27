from pydantic import BaseModel
from typing import Optional


class get_user_info(BaseModel):
    id:str
    frist_name:str
    last_name:str
    username:str
    role:str

class Insert_user_info(BaseModel):
    frist_name:str
    last_name:str
    username:str
    role:str

class Edit_user_info(BaseModel):
    id:str
    frist_name:str
    last_name:str
    username:str
    role:str
    created_at:str