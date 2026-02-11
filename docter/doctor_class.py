from pydantic import BaseModel
from typing import Optional

class create_doctor(BaseModel):
    user_id: str
    frist_name: str
    last_name: str

class edit_doctor(BaseModel):
    docter_id: str
    user_id: str
    frist_name: str
    last_name: str
    created_at:str
    edited_at: str