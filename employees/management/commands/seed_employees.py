"""
Management command to seed initial employee data for demonstration.
Creates 15 sample employees with realistic data.

Usage:
    python manage.py seed_employees
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from faker import Faker
import io
from PIL import Image
import random

from employees.models import Employee

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Seed initial employee data for the Employee Identity System'
    
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
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting employee data seeding...'))
        
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
        
        created_count = 0
        
        for i in range(1, 16):
            # Select random department
            department = random.choice(self.DEPARTMENTS)
            designation = random.choice(self.DESIGNATIONS[department])
            
            # Create employee
            employee_data = {
                'full_name': fake.name(),
                'designation': designation,
                'department': department,
                'date_of_joining': fake.date_between(start_date='-3y', end_date='today'),
                'status': 'ACTIVE',
                'created_by': admin_user,
            }
            
            try:
                # Generate a simple placeholder image
                img = self._generate_placeholder_image(
                    employee_data['full_name'],
                    200, 250
                )
                
                # Save image to ContentFile
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                img_file = ContentFile(
                    img_io.getvalue(),
                    name=f"employee_{i}_photo.png"
                )
                
                employee_data['employee_photo'] = img_file
                
                # Create employee
                employee = Employee.objects.create(**employee_data)
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created {employee.employee_id} - {employee.full_name} ({department})'
                    )
                )
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating employee {i}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully created {created_count} employees!'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nNote: These are placeholder photos generated for demonstration.'
            )
        )
    
    @staticmethod
    def _generate_placeholder_image(text, width=200, height=250):
        """
        Generate a simple placeholder image with employee initials.
        
        Args:
            text: Full name
            width: Image width
            height: Image height
            
        Returns:
            PIL Image object
        """
        # Create a new image with random background color
        colors = [
            '#667eea',  # Purple
            '#764ba2',  # Dark Purple
            '#f093fb',  # Pink
            '#4facfe',  # Blue
            '#00f2fe',  # Cyan
            '#43e97b',  # Green
            '#fa709a',  # Red
        ]
        
        bg_color = random.choice(colors)
        
        # Convert hex to RGB
        bg_color = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        img = Image.new('RGB', (width, height), color=bg_color)
        
        # Get initials
        names = text.split()
        initials = ''.join([n[0].upper() for n in names if n])[:2]
        
        # We won't actually draw text to keep dependencies minimal
        # Just return the colored image
        return img
