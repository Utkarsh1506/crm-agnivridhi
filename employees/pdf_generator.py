"""
Employee ID Card PDF Generation.
Generates professional, printable employee ID cards.
"""
from django.template.loader import render_to_string
from django.conf import settings
from xhtml2pdf import pisa
import io
import logging
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


class EmployeeIDCardPDF:
    """
    Generates professional employee ID cards in PDF format.
    Features:
    - Front side: Photo, Name, Designation, Employee ID
    - Back side: QR Code, Verification info, Company branding
    """
    
    PAPER_SIZE = 'A4'  # Standard paper size
    DPI = 300  # High-quality printing
    
    @staticmethod
    def generate_id_card_pdf(employee, include_back=True):
        """
        Generate a complete employee ID card PDF.
        
        Args:
            employee (Employee): Employee instance
            include_back (bool): Include back side with QR code
            
        Returns:
            ContentFile: PDF file as ContentFile object
            
        Raises:
            Exception: If PDF generation fails
        """
        try:
            # Prepare context for template
            context = {
                'employee': employee,
                'company_name': 'Agnivridhi',
                'include_back': include_back,
                'base_url': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'agnivridhi.com',
            }
            
            # Render HTML template
            html_string = render_to_string(
                'employees/id_card_pdf.html',
                context
            )
            
            # Generate PDF
            result = io.BytesIO()
            pisa_status = pisa.CreatePDF(
                html_string,
                dest=result,
                link_callback=EmployeeIDCardPDF.link_callback
            )
            
            if pisa_status.err:
                logger.error(f"PDF generation error for employee {employee.employee_id}")
                raise Exception("PDF generation failed")
            
            result.seek(0)
            filename = f"ID_Card_{employee.employee_id}.pdf"
            
            return ContentFile(result.getvalue(), name=filename)
        
        except Exception as e:
            logger.error(f"Failed to generate ID card for {employee.employee_id}: {str(e)}")
            raise
    
    @staticmethod
    def link_callback(uri, rel):
        """
        Callback to handle local file references in PDF.
        Converts relative URLs to absolute file paths.
        """
        if uri.startswith('http://') or uri.startswith('https://'):
            return uri
        
        # Handle static files
        if uri.startswith('/static/'):
            return f"{settings.STATIC_ROOT}{uri}"
        
        # Handle media files
        if uri.startswith('/media/'):
            return f"{settings.MEDIA_ROOT}{uri}"
        
        return uri
