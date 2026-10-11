import os
from dotenv import load_dotenv

from typing import Annotated
from fastapi import Depends, APIRouter, status,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from user_authenication.auth_service import authenticate_user,verify_jwt_access_token, userPasswordReset
from user_authenication.auth_class import AccessToken, EditUser


load_dotenv()

auth_router = APIRouter( prefix="/auth",tags=["Authenication Route"])
db_dependency = Annotated[Session, Depends(get_db)]
ex_time:int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
oauth2_bear = OAuth2PasswordBearer(tokenUrl='auth/token')


@auth_router.post("/token",response_model=AccessToken,description="This route handles user authenication",status_code=status.HTTP_200_OK)
async def user_authenication(from_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    return authenticate_user(db=db,username=from_data.username,password=from_data.password)

@auth_router.get("/get_token",status_code=status.HTTP_200_OK)
async def fetch_user_rle(db:db_dependency,token:Annotated[str,Depends(oauth2_bear)]):
    return verify_jwt_access_token(jwt_token=token,db=db)

@auth_router.post("/password_reset",status_code=status.HTTP_200_OK)
async def user_password_reset(db:db_dependency,value:EditUser,token:Annotated[str,Depends(oauth2_bear)]):
    result = verify_jwt_access_token(jwt_token=token,db=db)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    else:
        return userPasswordReset(user_edit=value,db=db)