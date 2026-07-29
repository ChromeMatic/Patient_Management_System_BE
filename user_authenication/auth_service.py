import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from modals.db_modals import Users
from pwdlib import PasswordHash

load_dotenv()

algorithm = os.getenv("ALGORITHM")
secret_key = os.getenv("SECRET_KEY")
minutes = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
hash_slat = os.getenv("SALT")
password_hash = PasswordHash.recommended()

# This function is responsible for password hashing
def get_password_hashed(plain_password:str):
    return password_hash.hash(password=plain_password)

# This function verify user password
def verify_user_password(plain_password:str,hashed_password) -> bool:
    return password_hash.verify(password=plain_password,hash=hashed_password)

# This user by user function get
def get_user_info(db:Session,username:str):
    try:
        user = db.query(Users).filter(
            Users.username == username
        ).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized User."
            )
        else:
            return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Please check user cred."
        )
    
# Verify JWT Access Token
def verify_jwt_access_token(jwt_token:str,db:Session):
    try:

        payload = jwt.decode(jwt_token,key=secret_key,algorithms=[algorithm])
        role:str = payload.get("sub")

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User's creditials could not be verified.",
                headers={"WWW-Authenticate":"Bearer"}
            )
        
        return  role
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in verifing JWT token: {err}"
        )


    
# Create JWT Access Token
def create_access_token(user:str,role:str, expires_delta:Optional[timedelta]):
   try:
        
        to_encode = { 'id':str(user),'sub':role }
        expires_at = datetime.now(timezone.utc) + expires_delta
        to_encode.update({'exp':expires_at})

        jwt_token = jwt.encode(payload=to_encode,key=secret_key,algorithm=algorithm)
        return jwt_token
   
   except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in JWT-Token creation: {err}"
        )
   
# Authenticate User
def   authenticate_user(db:Session, username:str, password:str):
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
       
        jwt_token = create_access_token(user=user.id,role=user.role,expires_delta=timedelta(minutes=(int(minutes))))

        return {
            "email_address": user.username,
            "access_token": jwt_token,
            "token_type": 'bearer'
        }
    
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Please check user cred: {err}"
        )