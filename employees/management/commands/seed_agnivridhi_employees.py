"""
Management command to seed employee data with Agnivridhi-specific employees.
Creates employees with provided IDs and names.

Usage:
    python manage.py seed_agnivridhi_employees
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
import io
from PIL import Image, ImageDraw, ImageFont
import random

from employees.models import Employee, EmployeeIDSequence
from employees.id_generator import EmployeeIDGenerator

User = get_user_model()

# Employee data: ID -> (Name, Designation)
EMPLOYEES = {
    '0101': ('Rahul Kumar Singh', 'CEO & Founder'),
    '0102': ('Urvashi Nandan Srivastava', 'Data Analyst'),
    '0103': ('Akash Tyagi', 'Branch Manager'),
    '0104': ('Harshit Tyagi', 'Manager'),
    '0105': ('Ayush Tomer', 'Business Development Executive'),
    '0106': ('Himadri Sharma', 'Business Development Executive'),
    '0107': ('Bhoomika Sharma', 'Business Development Executive'),
    '0108': ('Sharik Khan', 'Business Development Executive'),
    '0109': ('Rajdeep Singh', 'Team Leader'),
    '0110': ('Aaryav Singh', 'Business Development Executive'),
    '0111': ('Mohd Rihan', 'Business Development Executive'),
    '0112': ('Utkarsh Choudhary', 'Web Developer'),
    '0113': ('Rahul Kumar Pant', 'Business Development Executive'),
    '0114': ('Vaibhav Garg', 'Business Development Executive'),
    '0115': ('Babita Goswami', 'Business Development Executive'),
    '0116': ('Sanklp', 'Business Development Executive'),
    '0117': ('Vinay Kannaujiya', 'Business Development Executive'),
}

DEPARTMENTS = [
    'Sales',
    'Marketing',
    'Engineering',
    'Human Resources',
    'Finance',
    'Operations',
    'Management',
]

DESIGNATIONS = {
    'Sales': ['Sales Executive', 'Sales Manager', 'Regional Manager', 'Account Manager'],
    'Marketing': ['Marketing Specialist', 'Marketing Manager', 'Content Strategist', 'Brand Manager'],
    'Engineering': ['Junior Developer', 'Senior Developer', 'Tech Lead', 'Engineering Manager'],
    'Human Resources': ['HR Executive', 'HR Manager', 'Recruitment Manager', 'HR Head'],
    'Finance': ['Accountant', 'Finance Manager', 'CFO', 'Financial Analyst'],
    'Operations': ['Operations Executive', 'Operations Manager', 'Process Analyst', 'Operations Head'],
    'Management': ['Director', 'VP', 'CEO', 'Managing Director'],
}


class Command(BaseCommand):
    help = 'Seed Agnivridhi employee data with provided employee list'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Agnivridhi employee data seeding...'))
        
        # Get or create a system user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@agnivridhi.com',
                'first_name': 'System',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        # Reset the sequence to start from 117 (so next ID after 0117 will be 0118)
        sequence, _ = EmployeeIDSequence.objects.get_or_create(
            prefix='',
            defaults={'last_sequence_number': 117}
        )
        if sequence.last_sequence_number < 117:
            sequence.last_sequence_number = 117
            sequence.save()
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for emp_id, (full_name, designation) in EMPLOYEES.items():
            # Determine department based on designation
            department_map = {
                'CEO & Founder': 'Management',
                'Data Analyst': 'Finance',
                'Branch Manager': 'Operations',
                'Manager': 'Management',
                'Team Leader': 'Sales',
                'Web Developer': 'Engineering',
            }
            department = department_map.get(designation, 'Sales')
            
            # Check if employee already exists
            existing = Employee.objects.filter(employee_id=emp_id).first()
            if existing:
                # Update existing employee with new designation
                existing.designation = designation
                existing.department = department
                existing.save()
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated {emp_id} - {full_name} ({designation})')
                )
                updated_count += 1
                continue
            
            employee_data = {
                'full_name': full_name,
                'designation': designation,
                'department': department,
                'date_of_joining': timezone.now().date(),
                'status': 'ACTIVE',
                'created_by': admin_user,
                'employee_id': emp_id,
                'verification_token': EmployeeIDGenerator.generate_verification_token(),
            }
            
            try:
                # Generate a placeholder image with initials
                img = self._generate_placeholder_image(full_name, 200, 250)
                
                # Save image to ContentFile
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                img_file = ContentFile(
                    img_io.getvalue(),
                    name=f"employee_{emp_id}_photo.png"
                )
                
                employee_data['employee_photo'] = img_file
                
                # Create employee (bypass signals for ID generation since we're setting it manually)
                employee = Employee.objects.create(**employee_data)
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created {employee.employee_id} - {employee.full_name} ({department})'
                    )
                )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating {emp_id} ({full_name}): {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully created {created_count} employees!'
            )
        )
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'↻ Updated {updated_count} existing employees')
            )
    
    @staticmethod
    def _generate_placeholder_image(text, width=200, height=250):
        """
        Generate a placeholder image with employee initials and name.
        
        Args:
            text: Full name
            width: Image width
            height: Image height
            
        Returns:
            PIL Image object
        """
        colors = [
            (102, 126, 234),    # Purple
            (118, 75, 162),     # Dark Purple
            (240, 147, 251),    # Pink
            (79, 172, 254),     # Blue
            (0, 242, 254),      # Cyan
            (67, 233, 123),     # Green
            (250, 112, 154),    # Red
        ]
        
        bg_color = random.choice(colors)
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Get initials
        names = text.split()
        initials = ''.join([name[0].upper() for name in names])[:2]
        
        # Draw initials (centered, white text)
        try:
            # Try to use a larger font for initials
            font_size = 80
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Simple centering without using getbbox
        text_x = width // 2 - 40
        text_y = height // 3 - 40
        
        draw.text((text_x, text_y), initials, fill=(255, 255, 255), font=font)
        
        return img
