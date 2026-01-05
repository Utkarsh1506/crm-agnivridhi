"""
Barcode generation utility for Employee System.
Generates Code128 barcodes for employee IDs.
"""
import io
from PIL import Image, ImageDraw
import barcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)


class EmployeeBarcodeGenerator:
    """Generate barcodes for employee IDs."""
    
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
            # Create Code128 barcode
            # Older python-barcode versions on the server don't support add_checksum
            code128 = barcode.Code128(
                employee_id,
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
            
            logger.info(f"Generated barcode for employee {employee_id}")
            return ContentFile(output.getvalue(), name=f"barcode_{employee_id}.png")
            
        except Exception as e:
            logger.error(f"Failed to generate barcode for {employee_id}: {str(e)}")
            raise
