import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, text, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from database_config.db_config import Base


class UserRole(str, enum.Enum):
    SUPER = "supervisor"
    ADMIN = "admin"
    USER  = "regular"

class Users(Base):
    __tablename__="users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    frist_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    username = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(
        Enum(UserRole, name="user_role_enum"),
        nullable=False,
        default=UserRole.USER
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )