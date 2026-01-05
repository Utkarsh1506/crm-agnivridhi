"""
Barcode generation utility for Employee System.
Generates Code128 barcodes for employee IDs.
"""
import io
import os
import logging
from PIL import Image, ImageDraw
import barcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from django.conf import settings

logger = logging.getLogger(__name__)


class EmployeeBarcodeGenerator:
    """Generate barcodes for employee IDs."""

    @staticmethod
    def build_verification_url(employee_id):
        """Build public verification URL encoded in the barcode."""
        # Try multiple sources for base URL
        base_url = (
            os.getenv('PUBLIC_BASE_URL')
            or os.getenv('SITE_URL')
            or (f"https://agnivridhicrm.pythonanywhere.com" if os.getenv('PYTHONANYWHERE_DOMAIN') else None)
            or "https://agnivridhi.com"
        )
        return f"{base_url.rstrip('/')}/employees/verify/{employee_id}/"
    
    @staticmethod
    def generate_barcode(employee_id):
        """
        Generate a Code128 barcode for the employee ID.
        
        Args:
            employee_id: The employee ID to encode (e.g., '0101')
            
        Returns:
            ContentFile: PNG image of the barcode
        """
        try:
            # Encode the public verification URL so scan opens details page
            verify_url = EmployeeBarcodeGenerator.build_verification_url(employee_id)

            # Create Code128 barcode (no add_checksum for compatibility)
            code128 = barcode.Code128(
                verify_url,
                writer=ImageWriter()
            )
            
            # Generate image
            barcode_io = io.BytesIO()
            code128.write(barcode_io, options={'write_text': True, 'text_distance': 5})
            barcode_io.seek(0)
            
            # Convert to PIL Image to add employee ID text below
            img = Image.open(barcode_io)
            
            # Create final image with employee ID label
            final_img = Image.new('RGB', (img.width, img.height + 30), color='white')
            final_img.paste(img, (0, 0))
            
            # Add employee ID text
            draw = ImageDraw.Draw(final_img)
            text_x = (final_img.width - 60) // 2
            draw.text((text_x, img.height + 5), f"ID: {employee_id}", fill='black')
            
            # Save to ContentFile
            output = io.BytesIO()
            final_img.save(output, format='PNG')
            output.seek(0)
            
            logger.info(f"Generated barcode for employee {employee_id} -> {verify_url}")
            return ContentFile(output.getvalue(), name=f"barcode_{employee_id}.png")
            
        except Exception as e:
            logger.error(f"Failed to generate barcode for {employee_id}: {str(e)}")
            raise
