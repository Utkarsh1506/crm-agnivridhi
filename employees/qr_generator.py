"""
QR Code Generation Utilities.
Generates QR codes for employee verification without exposing personal data.
"""
import io
import qrcode
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)


class QRCodeGenerator:
    """
    Generates QR codes for employee verification.
    QR codes contain only verification URL, not personal information.
    """
    
    # QR Code Configuration
    QR_VERSION = 1  # Auto-detect, but start with version 1
    ERROR_CORRECTION = qrcode.constants.ERROR_CORRECT_H  # High error correction
    BOX_SIZE = 10  # Pixels per box
    BORDER = 2  # Border size in boxes
    
    @staticmethod
    def generate_qr_code(verification_url, filename=None):
        """
        Generate a QR code image for employee verification.
        
        Args:
            verification_url (str): Full URL to verification endpoint
                Example: https://agnivridhi.com/employee/verify/AGN-EMP-001/
            filename (str, optional): Filename for the QR code image
        
        Returns:
            ContentFile: Django ContentFile object containing QR code image
            
        Example:
            qr_file = QRCodeGenerator.generate_qr_code(
                'https://agnivridhi.com/employee/verify/AGN-EMP-001/',
                filename='agn-emp-001-qr.png'
            )
            employee.qr_code.save(filename, qr_file)
        """
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=QRCodeGenerator.QR_VERSION,
                error_correction=QRCodeGenerator.ERROR_CORRECTION,
                box_size=QRCodeGenerator.BOX_SIZE,
                border=QRCodeGenerator.BORDER,
            )
            
            # Add data and optimize
            qr.add_data(verification_url)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Generate filename if not provided
            if not filename:
                filename = 'employee_qr_code.png'
            
            # Return as ContentFile
            return ContentFile(img_byte_arr.getvalue(), name=filename)
        
        except Exception as e:
            logger.error(f"Failed to generate QR code: {str(e)}")
            raise
