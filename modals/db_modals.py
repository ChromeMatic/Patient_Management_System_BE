import uuid
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Boolean, String, Float, text, Enum, DateTime, Integer ,func
from sqlalchemy.dialects.postgresql import UUID
from database_config.db_config import Base

class userRole(str, enum.Enum):
    SUPER = "supervisor"
    ADMIN = "admin"
    DOC   = "doctor"
    NURSE = "nurse"
    ASS   = "clerk"
    USER  = "regular"

class appointment_status(str, enum.Enum):
    FT = "first_time"
    WI = "walk_in"
    FU = "follow_up"
    TM = "telemedicine"
    HV = "house_vist"

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
        Enum(userRole, name="user_role_enum"),
        nullable=False,
        default=userRole.USER
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

class UserRole(Base):
    __tablename__ = "user_role"

    user_role_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    role_name= Column(String,nullable=False)
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
    middle_name = Column(String,nullable=True)
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
    blood_pressure = relationship("Patient_Blood_Pressure_Vitals",back_populates="patient_bl_p_rec")
    history = relationship("Patients_Records",back_populates="records")

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
    pulse_oximetry = Column(Float,nullable=False)
    plus_rate = Column(Float,nullable=False)
    respiratory_rate = Column(Float,nullable=False)
    height = Column(Float,nullable=True)
    body_weight =  Column(Float,nullable=False)
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

class Patients_Records(Base):
    __tablename__ = "patient_records"

    record_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    patient_id = Column(UUID,ForeignKey("patient.patient_id"),nullable=False)
    presenting_complain = Column(String,nullable=False) 
    patient_diagnosis = Column(String,nullable=False)
    patient_treatment = Column(String,nullable=False)
    notes = Column(String,nullable=False)
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

    records = relationship("Patient",back_populates="history")

class Patient_File(Base):
    __tablename__ = "patient_files"

    file_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    patient_id = Column(UUID,ForeignKey("patient.patient_id"),nullable=False)
    url_link =  Column(String,nullable=False)
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

class Appointment_Table(Base):
    __tablename__ = "appointment_table"

    appointment_id= Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    patient_id = Column(UUID,ForeignKey("patient.patient_id"),nullable=False)
    appointment_type = Column(String,nullable=False)
    status = Column(String,nullable=False)
    date = Column(DateTime(timezone=True),nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

class Queue_table(Base):
    __tablename__ = "queue_table"

    queue_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    appointment_id = Column(UUID,ForeignKey("appointment_table.appointment_id"),nullable=False)
    slot_number = Column(Integer,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

class Organization_Table(Base):

    __tablename__ = "organization_table"

    org_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    Organization_name = Column(String,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

class Status_Table(Base):
    __tablename__ = "status_table"

    status_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        server_default=text("gen_random_uuid()")
    )
    status_name =  Column(String,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )