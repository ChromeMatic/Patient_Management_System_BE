import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

load_dotenv()

hash_slat = os.getenv("SALT")

password_hash = PasswordHash.recommended()

# This function is responsible for password hashing
def get_password_hashed(plain_password:str):
    return password_hash.hash(password=plain_password,salt=hash_slat)

# This function verify user password
def verify_user_password(plain_password:str,hashed_password):
    return password_hash.verify(password=plain_password,hash=hashed_password)