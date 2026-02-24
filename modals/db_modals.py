import uuid
import enum
from sqlalchemy import ForeignKey, Column, Boolean, String, text, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from database_config.db_config import Base


class UserRole(str, enum.Enum):
    SUPER = "supervisor"
    ADMIN = "admin"
    DOC   = "doctor"
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
    is_active = Column(Boolean,default=True,nullable=False)
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
    edited_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()
    )


class Docter(Base):

    __tablename__="docter_table"

    docter_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    frist_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    edited_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()
    )


class Patient(Base):

    __tablename__="patient"

    patient_id= Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    docter_id = Column(UUID,ForeignKey("docter_table.docter_id"),nullable=False)
    frist_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    DOB = Column(DateTime,nullable=False)
    TRN = Column(String, nullable=False)
    phone_number = Column(String,nullable=False)
    Address = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    edited_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()
    )


class Next_Of_Kin(Base):
    __tablename__="next_of_kin"

    next_of_kin_id= Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    patient_id = Column(UUID,ForeignKey("patient.patient_id"),nullable=False)
    frist_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    relation = Column(String,nullable=False)
    phone_number = Column(String,nullable=False)
    current_address = Column(String,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    edited_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now()
    )