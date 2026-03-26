import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Boolean, String, Float, text, Enum, DateTime, func
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
    docter_id = Column(UUID,ForeignKey("docter_table.docter_id"),nullable=True)
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

    relative = relationship("Next_Of_Kin",back_populates="kin")
    complaints = relationship("Presenting_Complain",back_populates="patient_com")
    blood_pressure = relationship("Patient_Blood_Pressure_Vitals",back_populates="patient_bl_p_rec")


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

    kin = relationship("Patient",back_populates="relative")
    


class Presenting_Complain(Base):
    __tablename__="presenting_complain"

    complaint_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    patient_id = Column(UUID,ForeignKey("patient.patient_id"),nullable=False)
    patient_complaint =  Column(String,nullable=False)
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

    patient_com = relationship("Patient",back_populates="complaints")


# Create patient record notes (vitals, medical notes, and file attachments)

class Patient_Blood_Pressure_Vitals(Base):
    __tablename__="patient_vitals"

    patient_vitals_id =  Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    patient_id = Column(UUID,ForeignKey("patient.patient_id"),nullable=False)
    blood_pressure_top_value = Column(Float,nullable=False)
    blood_pressure_bottom_value = Column(Float,nullable=False)
    body_temperature = Column(Float,nullable=False)
    plus_rate = Column(Float,nullable=False)
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

    patient_bl_p_rec = relationship("Patient",back_populates="blood_pressure")