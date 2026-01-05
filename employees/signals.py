"""
Employee Model Signals.
Handles automatic QR code generation, ID assignment, etc.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Employee
from .id_generator import EmployeeIDGenerator
from .qr_generator import QRCodeGenerator
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Employee)
def assign_employee_id_and_token(sender, instance, created, **kwargs):
    """
    Signal handler to assign unique employee ID and verification token
    when a new employee is created.
    
    This is called before saving, so we can set both fields.
    """
    if not instance.employee_id:  # Only for new employees
        try:
            instance.employee_id = EmployeeIDGenerator.generate_employee_id()
            instance.verification_token = EmployeeIDGenerator.generate_verification_token()
            logger.info(f"Assigned ID {instance.employee_id} to employee {instance.full_name}")
        except Exception as e:
            logger.error(f"Failed to assign employee ID: {str(e)}")
            raise


@receiver(post_save, sender=Employee)
def generate_employee_qr_code(sender, instance, created, **kwargs):
    """
    Signal handler to generate QR code after employee is saved.
    
    Runs AFTER save, so employee_id is guaranteed to exist.
    Uses post_save hook to ensure database commit before file generation.
    """
    if created:  # Only for new employees
        try:
            # Generate QR code with verification URL
            verification_url = instance.get_verification_url()
            qr_filename = f"{instance.employee_id}_qr.png"
            qr_content_file = QRCodeGenerator.generate_qr_code(
                verification_url,
                filename=qr_filename
            )
            
            # Save QR code to employee record
            instance.qr_code.save(qr_filename, qr_content_file, save=True)
            logger.info(f"Generated QR code for employee {instance.employee_id}")
        
        except Exception as e:
            logger.error(f"Failed to generate QR code for {instance.employee_id}: {str(e)}")
            # Don't raise - allow employee creation even if QR generation fails
            # QR can be regenerated later via admin action
