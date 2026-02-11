from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from user_authenication.auth_service import authenticate_user, create_access_token
from user_authenication.auth_class import user_credentials, Token

auth_router = APIRouter( prefix="/auth",tags=["Authenication Route"])
db_dependency = Annotated[Session, Depends(get_db)]


@auth_router.post("/token",status_code=status.HTTP_200_OK, response_class=Token)
def Authenicate_User(db:db_dependency,user:user_credentials):
    return authenticate_user(db=db,username=user.username,password=user.password)