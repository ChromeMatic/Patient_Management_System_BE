from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import Annotated
from database_config.db_config import get_db
from users.users_services import get_all_users, get_user_by_ID, get_user_by_usernme, create_new_user, edit_user_info
from users.users_class import Insert_user_info, Edit_user_info

user_endpoint = APIRouter( prefix="/user",tags=["User Endpoints"])
db_dependency = Annotated[Session, Depends(get_db)]

# This endpoint fetch all user infomation
@user_endpoint.get("/all-users/{limit:int}/{offset}",status_code=status.HTTP_200_OK)
def Fetch_all_users(db:db_dependency,limit:int,offset:int):
    return get_all_users(db=db,limit=limit,offset=offset)

# This endpoint fetch user by userId
@user_endpoint.get("/get-user-by-id/{user_id:str}",status_code=status.HTTP_200_OK)
def Fetch_user_by_user_Id(db:db_dependency,user_id:str):
    return get_user_by_ID(db=db,user_Id=user_id)

# This endpoint fetch user by username
@user_endpoint.get("/get-user-by-username/{username:str}",status_code=status.HTTP_200_OK)
def Fetch_user_by_username(db:db_dependency,username:str):
    return get_user_by_usernme(db=db,usernaame=username)

# This endpoint create new user
@user_endpoint.post("/create-new-user/",status_code=status.HTTP_201_CREATED)
def Create_new_user(db:db_dependency,new_user:Insert_user_info):
    return create_new_user(db=db,new_user=new_user)

# This endpoint edit user informtion
@user_endpoint.patch("/edit-user-info",status_code=status.HTTP_200_OK)
def Edit_user_infomation(db:db_dependency,userInfo:Edit_user_info):
    return edit_user_info(db=db,user_info=userInfo)