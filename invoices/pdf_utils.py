"""
Invoice PDF generation using ReportLab for professional output
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from io import BytesIO
from django.conf import settings
import os


class NumberedCanvas(canvas.Canvas):
    """Custom canvas with watermark"""
    def __init__(self, *args, **kwargs):
        self.watermark_text = kwargs.pop('watermark_text', 'Agnivridhi India')
        canvas.Canvas.__init__(self, *args, **kwargs)

    def showPage(self):
        self.save_state()
        # Add watermark
        self.setFont('Helvetica-Bold', 80)
        self.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.3)
        self.saveState()
        self.translate(A4[0]/2, A4[1]/2)
        self.rotate(45)
        self.drawCentredString(0, 0, self.watermark_text)
        self.restoreState()
        self.restore_state()
        canvas.Canvas.showPage(self)


def generate_invoice_pdf(invoice):
    """Generate professional invoice PDF using ReportLab"""
    buffer = BytesIO()
    
    # Create PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    # Container for elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#000000'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#444444')
    )
    
    invoice_type_style = ParagraphStyle(
        'InvoiceType',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#0066cc' if invoice.invoice_type == 'proforma' else '#006600'),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Header
    elements.append(Paragraph("AGNIVRIDHI INDIA", title_style))
    elements.append(Paragraph("Business Consultancy & Advisory Services", company_style))
    elements.append(Paragraph(
        "A-116, Urbtech Trade Centre, Sector-132, Chhaprauli Bengar<br/>"
        "Gautam Buddha Nagar, Dadri, Uttar Pradesh - 201304, India<br/>"
        "Email: account@agnivridhiindia.com | Phone: +91 92895 55190<br/>"
        "GSTIN: 09ABCCA3869R1ZU | PAN: ABCCA3869R | CIN: U70200UP2025PTC218739",
        company_style
    ))
    elements.append(Spacer(1, 10*mm))
    
    # Invoice type
    inv_type = "PROFORMA INVOICE" if invoice.invoice_type == 'proforma' else "TAX INVOICE"
    elements.append(Paragraph(inv_type, invoice_type_style))
    elements.append(Spacer(1, 5*mm))
    
    # Invoice meta data
    meta_data = [
        ['Invoice No:', invoice.invoice_number, 'Invoice Date:', invoice.issue_date.strftime('%d %b %Y')],
        ['Page:', '1 of 1', '', '']
    ]
    meta_table = Table(meta_data, colWidths=[40*mm, 50*mm, 40*mm, 50*mm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 5*mm))
    
    # Billing information
    if invoice.client:
        address_parts = []
        if invoice.client.address_line1:
            address_parts.append(invoice.client.address_line1)
        if invoice.client.address_line2:
            address_parts.append(invoice.client.address_line2)
        address_str = ', '.join(address_parts) if address_parts else '-'
        
        bill_to = f"<b>{invoice.client.company_name.upper()}</b><br/>" \
                  f"{invoice.client.contact_person}<br/>" \
                  f"{address_str}<br/>" \
                  f"{invoice.client.city}, {invoice.client.state} - {invoice.client.pincode}<br/>" \
                  f"GSTIN: {invoice.client.gstin or 'Unregistered'}<br/>" \
                  f"Contact: {invoice.client.mobile}"
    else:
        bill_to = f"<b>{invoice.client_name.upper() if invoice.client_name else 'N/A'}</b><br/>"
        if invoice.client_contact_person:
            bill_to += f"{invoice.client_contact_person}<br/>"
        if invoice.client_address:
            bill_to += f"{invoice.client_address}<br/>"
        if invoice.client_city or invoice.client_state:
            bill_to += f"{invoice.client_city or ''}, {invoice.client_state or ''}"
            if invoice.client_pincode:
                bill_to += f" - {invoice.client_pincode}"
            bill_to += "<br/>"
        bill_to += f"GSTIN: {invoice.client_gstin or 'Unregistered'}<br/>"
        if invoice.client_mobile:
            bill_to += f"Contact: {invoice.client_mobile}"
    
    bill_from = "<b>AGNIVRIDHI INDIA</b><br/>" \
                "A-116, Urbtech Trade Centre, Sector-132<br/>" \
                "Chhaprauli Bengar, Gautam Buddha Nagar<br/>" \
                "Dadri, Uttar Pradesh - 201304, India<br/>" \
                "GSTIN: 09ABCCA3869R1ZU<br/>" \
                "Email: account@agnivridhiindia.com<br/>" \
                "Phone: +91 92895 55190"
    
    billing_data = [[
        Paragraph("<b>BILLED TO</b><br/><br/>" + bill_to, styles['Normal']),
        Paragraph("<b>BILLED FROM</b><br/><br/>" + bill_from, styles['Normal'])
    ]]
    
    billing_table = Table(billing_data, colWidths=[90*mm, 90*mm])
    billing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(billing_table)
    elements.append(Spacer(1, 5*mm))
    
    # Items table
    items_data = [
        ['#', 'Description', 'HSN/SAC', 'Qty', 'Rate (Rs.)', 'Amount (Rs.)']
    ]
    items_data.append([
        '1',
        invoice.item_description,
        invoice.hsn_sac,
        str(int(invoice.quantity)),
        f"{invoice.rate:.2f}",
        f"{invoice.taxable_amount:.2f}"
    ])
    
    items_table = Table(items_data, colWidths=[10*mm, 70*mm, 25*mm, 15*mm, 30*mm, 30*mm])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 3*mm))
    
    # Totals table (right aligned)
    totals_data = [
        ['Taxable Amount:', f"Rs. {invoice.taxable_amount:.2f}"]
    ]
    
    if invoice.cgst_amount > 0:
        totals_data.append([f'CGST @ {invoice.gst_rate/2:.1f}%:', f"Rs. {invoice.cgst_amount:.2f}"])
        totals_data.append([f'SGST @ {invoice.gst_rate/2:.1f}%:', f"Rs. {invoice.sgst_amount:.2f}"])
    
    if invoice.igst_amount > 0:
        totals_data.append([f'IGST @ {invoice.gst_rate:.0f}%:', f"Rs. {invoice.igst_amount:.2f}"])
    
    totals_data.append(['Total Amount:', f"Rs. {invoice.total_amount:.2f}"])
    
    totals_table = Table(totals_data, colWidths=[60*mm, 30*mm])
    totals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -2), colors.HexColor('#f5f5f5')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, -2), colors.black),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -2), 9),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    # Right align totals
    totals_wrapper = Table([[' ', totals_table]], colWidths=[90*mm, 90*mm])
    totals_wrapper.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(totals_wrapper)
    elements.append(Spacer(1, 5*mm))
    
    # Notes
    if invoice.notes:
        notes_style = ParagraphStyle('Notes', parent=styles['Normal'], fontSize=9, leftIndent=10, rightIndent=10)
        elements.append(Paragraph(f"<b>Additional Notes:</b><br/>{invoice.notes}", notes_style))
        elements.append(Spacer(1, 5*mm))
    
    # Signature for tax invoice
    if invoice.invoice_type == 'tax':
        elements.append(Spacer(1, 10*mm))
        sig_data = [['', 'For AGNIVRIDHI INDIA'], ['', ''], ['', ''], ['', 'Authorized Signatory']]
        sig_table = Table(sig_data, colWidths=[90*mm, 90*mm])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTSIZE', (1, 0), (1, 0), 10),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (1, -1), (1, -1), 9),
            ('LINEABOVE', (1, -1), (1, -1), 1, colors.black),
        ]))
        elements.append(sig_table)
    
    # Disclaimer for proforma
    if invoice.invoice_type == 'proforma':
        disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=8, 
                                         textColor=colors.HexColor('#666666'), fontName='Helvetica-Oblique',
                                         leftIndent=10, rightIndent=10, spaceBefore=10, spaceAfter=10,
                                         borderColor=colors.HexColor('#ffc107'), borderWidth=0,
                                         borderPadding=8, backColor=colors.HexColor('#f9f9f9'))
        elements.append(Paragraph(
            "<b>Note:</b> This is a Proforma Invoice issued for estimation and documentation purposes only. "
            "It is not a demand for payment and is subject to change at the time of final Tax Invoice.",
            disclaimer_style
        ))
    
    # Footer
    elements.append(Spacer(1, 10*mm))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                                  alignment=TA_CENTER, textColor=colors.HexColor('#666666'))
    elements.append(Paragraph(
        "<b>This is an electronically generated document, no signature is required.</b><br/>"
        "Terms & Conditions: Payment due within 15 days. All disputes subject to jurisdiction of courts in Noida.<br/>"
        "Thank you for your business!",
        footer_style
    ))
    
    # Build PDF with watermark
    doc.build(elements, canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, watermark_text='Agnivridhi India', **kwargs))
    
    buffer.seek(0)
    return buffer
