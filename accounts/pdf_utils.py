"""
PDF generation utilities for Agnivridhi CRM
Uses ReportLab for generating professional PDFs

Supported Documents:
- Payment Receipts
- Booking Confirmations
- Application Forms
- DPR Reports
- Invoices
"""

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_pdf_from_html(html_string, filename='document.pdf'):
    """
    Placeholder for HTML to PDF conversion (not used with ReportLab)
    """
    pass


def generate_payment_receipt_pdf(payment):
    """
    Generate payment receipt PDF using ReportLab
    
    Args:
        payment: Payment object
    
    Returns:
        HttpResponse: PDF receipt
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#008080'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph('PAYMENT RECEIPT', title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Company info
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER
    )
    elements.append(Paragraph('Agnivridhi India', company_style))
    elements.append(Paragraph('info@agnivridhiindia.com', company_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Payment details table
    data = [
        ['Receipt #:', str(payment.reference_id or payment.id)],
        ['Date:', datetime.now().strftime('%Y-%m-%d')],
        ['Client:', payment.client.company_name],
        ['Amount:', f'₹{payment.amount:,.2f}'],
        ['Mode:', payment.payment_mode],
        ['Status:', payment.approval_status],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph('Thank you for your payment!', company_style))
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'Receipt_{payment.reference_id or payment.id}_{datetime.now().strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def generate_booking_confirmation_pdf(booking):
    """
    Generate booking confirmation PDF using ReportLab
    
    Args:
        booking: Booking object
    
    Returns:
        HttpResponse: PDF confirmation
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066CC'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph('BOOKING CONFIRMATION', title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Booking details table
    data = [
        ['Booking ID:', str(booking.id)],
        ['Date:', booking.booking_date.strftime('%Y-%m-%d')],
        ['Client:', booking.client.company_name],
        ['Service:', booking.service.name],
        ['Amount:', f'₹{booking.service.base_price:,.2f}'],
        ['Status:', booking.status],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    
    if booking.notes:
        elements.append(Paragraph('<b>Notes:</b>', styles['Normal']))
        elements.append(Paragraph(booking.notes, styles['Normal']))
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'Booking_{booking.id}_{datetime.now().strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def generate_application_form_pdf(application):
    """
    Generate application form PDF using ReportLab
    
    Args:
        application: Application object
    
    Returns:
        HttpResponse: PDF application form
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#006600'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph('APPLICATION FORM', title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Application details
    data = [
        ['Application ID:', str(application.id)],
        ['Date:', application.application_date.strftime('%Y-%m-%d')],
        ['Client:', application.client.company_name],
        ['Scheme:', application.scheme.name],
        ['Amount:', f'₹{application.amount_requested:,.2f}'],
        ['Status:', application.status],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'Application_{application.id}_{datetime.now().strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def generate_dpr_report_pdf(client, date_from=None, date_to=None):
    """
    Generate DPR (Daily Progress Report) PDF using ReportLab
    
    Args:
        client: Client object
        date_from: Start date filter
        date_to: End date filter
    
    Returns:
        HttpResponse: PDF DPR report
    """
    from bookings.models import Booking
    from payments.models import Payment
    from applications.models import Application
    
    bookings = Booking.objects.filter(client=client)
    payments = Payment.objects.filter(client=client)
    applications = Application.objects.filter(client=client)
    
    if date_from:
        bookings = bookings.filter(booking_date__gte=date_from)
        payments = payments.filter(payment_date__gte=date_from)
        applications = applications.filter(application_date__gte=date_from)
    
    if date_to:
        bookings = bookings.filter(booking_date__lte=date_to)
        payments = payments.filter(payment_date__lte=date_to)
        applications = applications.filter(application_date__lte=date_to)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#CC6600'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph('DAILY PROGRESS REPORT', title_style))
    elements.append(Paragraph(f'Client: {client.company_name}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary
    total_payments = sum(p.amount for p in payments) if payments else 0
    data = [
        ['Total Bookings:', str(bookings.count())],
        ['Total Payments:', f'₹{total_payments:,.2f}'],
        ['Total Applications:', str(applications.count())],
        ['Report Date:', datetime.now().strftime('%Y-%m-%d')],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.orange),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'DPR_{client.company_name}_{datetime.now().strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def generate_invoice_pdf(payment):
    """
    Generate invoice PDF for payment using ReportLab
    
    Args:
        payment: Payment object
    
    Returns:
        HttpResponse: PDF invoice
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#990000'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    elements.append(Paragraph('INVOICE', title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Invoice details
    invoice_number = f'INV-{payment.id:06d}'
    data = [
        ['Invoice #:', invoice_number],
        ['Date:', datetime.now().strftime('%Y-%m-%d')],
        ['Client:', payment.client.company_name],
        ['Service:', payment.booking.service.name if payment.booking else 'N/A'],
        ['Amount:', f'₹{payment.amount:,.2f}'],
        ['Payment Mode:', payment.payment_mode],
        ['Status:', payment.approval_status],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.pink),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph('Agnivridhi India', styles['Normal']))
    elements.append(Paragraph('info@agnivridhiindia.com', styles['Normal']))
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'Invoice_{payment.reference_id or payment.id}_{datetime.now().strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

