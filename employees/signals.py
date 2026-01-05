"""
Employee Model Signals.
Handles automatic barcode generation, ID assignment, etc.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Employee
from .id_generator import EmployeeIDGenerator
from .barcode_utils import EmployeeBarcodeGenerator
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Employee)
def assign_employee_id_and_token(sender, instance, **kwargs):
    """
    Signal handler to assign unique employee ID and verification token
    when a new employee is created.
    
    This is called before saving, so we can set both fields.
    Note: pre_save doesn't have 'created' parameter, we check if pk is None.
    """
    if not instance.employee_id:  # Only for new employees (no ID set yet)
        try:
            instance.employee_id = EmployeeIDGenerator.generate_employee_id()
            instance.verification_token = EmployeeIDGenerator.generate_verification_token()
            logger.info(f"Assigned ID {instance.employee_id} to employee {instance.full_name}")
        except Exception as e:
            logger.error(f"Failed to assign employee ID: {str(e)}")
            raise


@receiver(post_save, sender=Employee)
def generate_employee_barcode(sender, instance, created, **kwargs):
    """
    Signal handler to generate barcode after employee is saved.
    
    Runs AFTER save, so employee_id is guaranteed to exist.
    Uses post_save hook to ensure database commit before file generation.
    """
    if created:  # Only for new employees
        try:
            # Generate barcode with employee ID
            barcode_filename = f"{instance.employee_id}_barcode.png"
            barcode_content_file = EmployeeBarcodeGenerator.generate_barcode(
                instance.employee_id
            )
            
            # Save barcode to employee record
            instance.barcode.save(barcode_filename, barcode_content_file, save=True)
            logger.info(f"Generated barcode for employee {instance.employee_id}")
        
        except Exception as e:
            logger.error(f"Failed to generate barcode for {instance.employee_id}: {str(e)}")
            # Don't raise - allow employee creation even if barcode generation fails
            # Barcode can be regenerated later via admin action
