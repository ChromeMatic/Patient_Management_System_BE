import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from modals.db_modals import Patient, Next_Of_Kin, Patients_Records
from patient.patient_class import insert_patient,edit_patient, next_of_kin, Patient_Search
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

# This function gets all patients from Database
def get_all_patients(db:Session,limnit:int,offset:int):
    return db.query(Patient).order_by(Patient.created_at.desc()).limit(limit=limnit).offset(offset=offset).all()

# This function get patient by ID
def get_patient_by_ID(db:Session,Id:str):
    return (
        db.query(Patient)
        .options(
            joinedload(Patient.relative),
            joinedload(Patient.history)
        )
        .filter(Patient.patient_id == Id)
        .first()
    )

# This function gets all next of kin records
def get_all_next_of_kin_record(db:Session,limnit:int,offset:int):
    return db.query(Next_Of_Kin).limit(limit=limnit).offset(offset=offset).order_by(Next_Of_Kin.created_at.desc()).all()

# This function gets all Patient by docter ID    
def get_patients_by_docter(db:Session,doctor_id:str,limnit:int,offset:int):
    try:
        result = db.query(Patient).filter(
            Patient.docter_id ==  doctor_id
        ).limit(limit=limnit).offset(offset=offset).all()

        return result
    except Exception:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in Fetching patient database."
        )
    
# This function creates a new patient
def create_new_patient(db:Session,new_record:insert_patient,new_kin:next_of_kin):
    try:
        new_patient = Patient(
            frist_name = new_record.frist_name,
            last_name = new_record.last_name,
            middle_name = new_record.middle_name,
            DOB = new_record.DOB,
            TRN = new_record.TRN,
            Address =  new_record.Address,
            phone_number = new_record.phone_number
        )

        db.add(new_patient)
        db.flush()

        record = Next_Of_Kin(
           patient_id = new_patient.patient_id,
           frist_name = new_kin.frist_name,
           last_name = new_kin.last_name,
           relation = new_kin.relation,
           phone_number = new_kin.phone_number,
           current_address = new_kin.current_address
        )
        
        db.add(record)
        
        db.commit()
        db.refresh(new_patient)

        return "New Patient and Next of Kin record added."
    except Exception as err:
          db.rollback()
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in create new patient in database: {err}"
        )

# This funtion edit patient record
def edit_patient_record(db:Session,record:edit_patient):
    try:
        patient_record = get_patient_by_ID(db=db,Id=record.patient_id)

        patient_record.frist_name = record.frist_name
        patient_record.last_name = record.last_name 
        patient_record.middle_name = record.middle_name
        patient_record.DOB = record.DOB
        patient_record.TRN = record.TRN
        patient_record.Address = record.Address
        patient_record.edited_at =  func.now()

        db.commit()
        db.refresh(patient_record)

        return "Patient record has been edited."
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in editing patient record."
        )    

# This handles seach of patient
def search_by(db:Session,value:Patient_Search):
    try:

        if value.frist_name is None and value.last_name is None:
            result = db.query(Patient).filter(
                Patient.TRN.ilike(f"%{value.TRN}%")
            ).limit(limit=value.limit).offset(offset=value.offset).all()

        if value.frist_name is not None and value.last_name is None and value.TRN is None:
            result = db.query(Patient).filter(
                Patient.frist_name.ilike(f"%{value.frist_name}%")
            ).limit(limit=value.limit).offset(offset=value.offset).all()
             
        if value.last_name is not None and value.frist_name is None and value.TRN is None:
            result = db.query(Patient).filter(
                Patient.last_name.ilike(f"%{value.last_name}%")
            ).limit(limit=value.limit).offset(offset=value.offset).all()

        if value.last_name is not None and value.frist_name is not None and value.TRN is None:
            result = db.query(Patient).filter(
                Patient.last_name.ilike(f"%{value.last_name}%"),
                Patient.frist_name.ilike(f"%{value.frist_name}%")
            ).limit(limit=value.limit).offset(offset=value.offset).all()

        return result

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in editing patient record."
    )        

# This function print records
def genrate_patient_document(db: Session, patientId: str):
    # Get data from database
    info = get_patient_by_ID(db=db, Id=patientId)
    if not info:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Create an in-memory buffer for the PDF
    buffer = io.BytesIO()
    
    # Setup document template
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=34, 
        leftMargin=34, 
        topMargin=34, 
        bottomMargin=34
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor("#2C3E50"),
        spaceAfter=15
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor("#34495E"),
        spaceBefore=12,
        spaceAfter=6
    )
    
    normal_style = styles['Normal']

    # --- Add Logo ---
    try:
        logo = Image("aurion_logo_bg_trans.png", width=140, height=60)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 10))
    except Exception as e:
        print(f"Could not load logo: {e}")

    # --- Header Title ---
    story.append(Paragraph("Patient Medical Report", title_style))
    story.append(Spacer(1, 5))

    # --- Personal Information Section ---
    story.append(Paragraph("Personal Information", section_style))
    
    # Format full name safely handling middle name if present
    middle = f" {info.middle_name}" if info.middle_name else ""
    full_name = f"{info.frist_name}{middle} {info.last_name}"
    
    patient_data = [
        [Paragraph("<b>Full Name:</b>", normal_style), Paragraph(full_name, normal_style)],
        [Paragraph("<b>DOB:</b>", normal_style), Paragraph(str(info.DOB or 'N/A'), normal_style)],
        [Paragraph("<b>TRN:</b>", normal_style), Paragraph(str(info.TRN or 'N/A'), normal_style)],
        [Paragraph("<b>Phone Number:</b>", normal_style), Paragraph(str(info.phone_number or 'N/A'), normal_style)],
        [Paragraph("<b>Address:</b>", normal_style), Paragraph(str(info.Address or 'N/A'), normal_style)],
    ]
    
    t1 = Table(patient_data, colWidths=[120, 400])
    t1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    # --- Relative / Next of Kin Section (Iterating through list) ---
    if info.relative:
        story.append(Paragraph("Emergency Contacts / Relatives", section_style))
        
        for rel in info.relative:
            rel_middle = f" {rel.middle_name}" if hasattr(rel, 'middle_name') and rel.middle_name else ""
            rel_name = f"{rel.frist_name}{rel_middle} {rel.last_name}"
            
            relative_data = [
                [Paragraph("<b>Name:</b>", normal_style), Paragraph(rel_name, normal_style)],
                [Paragraph("<b>Relation:</b>", normal_style), Paragraph(str(rel.relation or 'N/A'), normal_style)],
                [Paragraph("<b>Phone:</b>", normal_style), Paragraph(str(rel.phone_number or 'N/A'), normal_style)],
                [Paragraph("<b>Address:</b>", normal_style), Paragraph(str(rel.current_address or 'N/A'), normal_style)],
            ]
            
            t_rel = Table(relative_data, colWidths=[120, 400])
            t_rel.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.HexColor("#E2E8F0"))
            ]))
            story.append(t_rel)
            story.append(Spacer(1, 8))

    # --- Medical History Section ---
    story.append(Paragraph("Medical History", section_style))
    if info.history and len(info.history) > 0:
        history_rows = [["Date", "Description"]]
        for h in info.history:
            history_rows.append([
                Paragraph(str(getattr(h, 'date', 'N/A')), normal_style), 
                Paragraph(str(getattr(h, 'description', 'N/A')), normal_style)
            ])
        
        t3 = Table(history_rows, colWidths=[120, 400])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ECF0F1")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#2C3E50")),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7"))
        ]))
        story.append(t3)
    else:
        story.append(Paragraph("<i>No medical history records found.</i>", normal_style))

    # Build PDF
    doc.build(story)
    
    # Reset buffer pointer to the beginning
    buffer.seek(0)
    return buffer