"""
Employee ID Generation Utilities.
Handles unique, auto-incrementing employee ID generation with thread safety.
"""
from django.db import transaction
from .models import Employee, EmployeeIDSequence
import uuid


class EmployeeIDGenerator:
    """
    Thread-safe Employee ID generator.
    Generates unique IDs in format: 0101, 0102, etc.
    """
    
    PREFIX = ''
    PADDING = 4  # Zero-padding: 0101, 0102, etc.
    
    @staticmethod
    @transaction.atomic
    def generate_employee_id():
        """
        Generate next employee ID in sequence.
        
        Uses database transaction to ensure thread-safety and uniqueness.
        
        Returns:
            str: Generated employee ID (e.g., '0101', '0102')
            
        Raises:
            Exception: If sequence generation fails
        """
        # Get or create the sequence tracker
        sequence, created = EmployeeIDSequence.objects.get_or_create(
            prefix=EmployeeIDGenerator.PREFIX
        )
        
        # Increment and generate ID
        sequence.last_sequence_number += 1
        employee_id = f"{sequence.PREFIX}{sequence.last_sequence_number:0{EmployeeIDGenerator.PADDING}d}"
        
        # Save the updated sequence
        sequence.save()
        
        return employee_id
    
    @staticmethod
    def get_next_sequence_number():
        """Get the next sequence number without incrementing."""
        sequence, _ = EmployeeIDSequence.objects.get_or_create(
            prefix=EmployeeIDGenerator.PREFIX
        )
        return sequence.last_sequence_number + 1
    
    @staticmethod
    def generate_verification_token():
        """
        Generate a unique verification token for public access.
        This token is used in the verification URL instead of employee ID.
        
        Returns:
            str: Unique verification token
        """
        return str(uuid.uuid4())
