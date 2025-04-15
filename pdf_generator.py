from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from io import BytesIO
import datetime
from constants import TIMEZONE

def add_watermark(canvas, doc, watermark_path, opacity=0.2):
    if watermark_path:
        watermark = ImageReader(watermark_path)
        canvas.saveState()
        if hasattr(canvas, 'setFillAlpha'):
            canvas.setFillAlpha(opacity)
        else:
            canvas.setAlpha(opacity)
        canvas.drawImage(watermark, x=150, y=300, width=300, height=300, mask='auto')
        canvas.restoreState()

def generate_treatment_pdf(disease, disease_data, username):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'], fontSize=20, spaceAfter=12, textColor=HexColor('#1e293b'), fontName='Helvetica-Bold', alignment=1
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Heading2'], fontSize=14, spaceBefore=12, spaceAfter=6, textColor=HexColor('#3b82f6'), fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontSize=12, spaceAfter=6, textColor=HexColor('#0f172a'), leading=14
    )
    
    story = []
    story.append(Paragraph("HeyDoc Treatment Plan Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    today = datetime.datetime.now(TIMEZONE).strftime("%B %d, %Y, %H:%M +0530")
    story.append(Paragraph(f"Generated for: {username}", body_style))
    story.append(Paragraph(f"Date: {today}", body_style))
    story.append(Paragraph(f"Report by {username} by HeyDoc on {today}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    drawing = Drawing(400, 1)
    drawing.add(Line(0, 0, 400, 0, strokeColor=HexColor('#334155'), strokeWidth=1))
    story.append(drawing)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Predicted Condition", section_style))
    story.append(Paragraph(disease, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    if disease_data and "treatment" in disease_data:
        story.append(Paragraph("Treatment Plan", section_style))
        for treatment in disease_data["treatment"]:
            story.append(Paragraph(f"• {treatment}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    if disease_data and "prevention" in disease_data:
        story.append(Paragraph("Prevention Tips", section_style))
        for prevention in disease_data["prevention"]:
            story.append(Paragraph(f"• {prevention}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("When to See a Doctor", section_style))
    story.append(Paragraph("Consult a healthcare provider if symptoms persist or worsen.", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    doc.build(story, onFirstPage=lambda c, d: add_watermark(c, d, "heydoc-high-resolution-logo.png"), 
             onLaterPages=lambda c, d: add_watermark(c, d, "heydoc-high-resolution-logo.png"))
    
    buffer.seek(0)
    return buffer

def generate_illness_pdf(disease, disease_data, username):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'], fontSize=20, spaceAfter=12, textColor=HexColor('#1e293b'), fontName='Helvetica-Bold', alignment=1
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Heading2'], fontSize=14, spaceBefore=12, spaceAfter=6, textColor=HexColor('#3b82f6'), fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontSize=12, spaceAfter=6, textColor=HexColor('#0f172a'), leading=14
    )
    
    story = []
    story.append(Paragraph("HeyDoc Illness Information Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    today = datetime.datetime.now(TIMEZONE).strftime("%B %d, %Y, %H:%M +0530")
    story.append(Paragraph(f"Generated for: {username}", body_style))
    story.append(Paragraph(f"Date: {today}", body_style))
    story.append(Paragraph(f"Report by {username} by HeyDoc on {today}", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    drawing = Drawing(400, 1)
    drawing.add(Line(0, 0, 400, 0, strokeColor=HexColor('#334155'), strokeWidth=1))
    story.append(drawing)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Condition", section_style))
    story.append(Paragraph(disease, body_style))
    story.append(Spacer(1, 0.1*inch))
    
    if disease_data and "definition" in disease_data:
        story.append(Paragraph("Description", section_style))
        for desc in disease_data["definition"]:
            story.append(Paragraph(f"• {desc}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    if disease_data and "symptoms" in disease_data:
        story.append(Paragraph("Common Symptoms", section_style))
        for symptom in disease_data["symptoms"]:
            story.append(Paragraph(f"• {symptom}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    if disease_data and "causes" in disease_data:
        story.append(Paragraph("Causes", section_style))
        for cause in disease_data["causes"]:
            story.append(Paragraph(f"• {cause}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    if disease_data and "risk_factors" in disease_data:
        story.append(Paragraph("Risk Factors", section_style))
        for risk in disease_data["risk_factors"]:
            story.append(Paragraph(f"• {risk}", body_style))
        story.append(Spacer(1, 0.1*inch))
    
    doc.build(story, onFirstPage=lambda c, d: add_watermark(c, d, "heydoc-high-resolution-logo.png"), 
             onLaterPages=lambda c, d: add_watermark(c, d, "heydoc-high-resolution-logo.png"))
    
    buffer.seek(0)
    return buffer