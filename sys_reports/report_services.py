import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from modals.db_modals import Patient, Appointment_Table
from sqlalchemy import func
from sqlalchemy.orm import Session

#This funtion create basic report
def grenerate_basic_pdf_report(db:Session):

    total_p_number = db.query(func.count(Patient.patient_id)).scalar() or 0
    total_a_number = db.query(func.count(Appointment_Table.appointment_id)).scalar() or 0
 
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
    story.append(Paragraph("Information", section_style))
        
    patient_data = [
        [Paragraph("<b>Total number of Patients:</b>", normal_style), Paragraph(str(total_p_number),normal_style)],
        [Paragraph("<b>Total number of Appointments:</b>", normal_style), Paragraph(str(total_a_number),normal_style)],
    ]

    t1 = Table(patient_data, colWidths=[120, 400])
    t1.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    # Build PDF
    doc.build(story)
        
    # Reset buffer pointer to the beginning
    buffer.seek(0)
    return buffer
        