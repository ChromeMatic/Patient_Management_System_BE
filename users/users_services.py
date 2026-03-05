from users_class import Insert_user_info,Edit_user_info
from modals.db_modals import Users,UserRole
from user_authenication.auth_service import get_password_hashed
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# This function gets all patients from Database
def get_all_users(db:Session,limnit:int,offset:int):
    return db.query(Users).limit(limit=limnit).offset(offset=offset).all()

# This function get patient by ID
def get_patient_by_ID(db:Session,user_Id:str):
    return db.query(Users).filter(Users.id == user_Id).first()

# This function get patient by usernme [email address]
def get_patient_by_usernme(db:Session,usernaame:str):
    return db.query(Users).filter(Users.username == usernaame).first()

# This function adds new user to databse table
def create_new_user(db:Session,new_user:Insert_user_info):
    try:

        user = Users(
            frist_name = new_user.frist_name,
            last_name = new_user.last_name,
            username = new_user.username,
            password = get_password_hashed(new_user.password),
            role = UserRole.USER
        )

        db.add(user)
        db.commit()

        return "New User added."
    except Exception:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in creating new user."
        )
