import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from modals.db_modals import Users
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

load_dotenv()

algorithm = os.getenv("ALGORITHM")
secret_key = os.getenv("SECRET_KEY")
minutes = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
hash_slat = os.getenv("SALT")
password_hash = PasswordHash.recommended()

# This function is responsible for password hashing
def get_password_hashed(plain_password:str):
    return password_hash.hash(password=plain_password,salt=10)

# This function verify user password
def verify_user_password(plain_password:str,hashed_password) -> bool:
    return password_hash.verify(password=plain_password,hash=hashed_password)

# This user by user function get
def get_user_info(db:Session,username:str):
    try:
        user = db.query(Users).filter(
            Users.username == username
        ).first()

        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Please check user cred."
        )
    
# Verify JWT Access Token
def verify_jwt_access_token(jwt_token:str):
    try:

        payload = jwt.decode(jwt_token,key=secret_key,algorithms=[algorithm])
        email:str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User's creditials could not be verified."
            )

    
# Create JWT Access Token
def create_access_token(user_data:dict, expires_delta:Optional[timedelta]=None):
    try:
        to_encode = user_data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        
        to_encode.update({"exp":expire})
        encoded_web_token = jwt.encode(payload=to_encode,key=secret_key,algorithm=algorithm)

        return encoded_web_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when generating JWT token."
        )

# Authenticate User
def authenticate_user(db:Session, username:str, password:str):
    try:
        user = get_user_info(db=db,username=username)

        if not user:
            raise HTTPException( 
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        if not verify_user_password(plain_password=password,hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password."
            )
        return user
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Please check user cred."
        )
    
