"""
Management command to update employee designations.
Allows updating designations for existing employees.

Usage:
    python manage.py update_employee_designations
"""
from django.core.management.base import BaseCommand
from employees.models import Employee

# Designation mappings
EMPLOYEE_DESIGNATIONS = {
    '0101': {'designation': 'CEO & Founder', 'department': 'Management'},
    '0102': {'designation': 'Data Analyst', 'department': 'Finance'},
    '0103': {'designation': 'Branch Manager', 'department': 'Operations'},
    '0104': {'designation': 'Manager', 'department': 'Management'},
    '0105': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0106': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0107': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0108': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0109': {'designation': 'Team Leader', 'department': 'Sales'},
    '0110': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0111': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0112': {'designation': 'Web Developer', 'department': 'Engineering'},
    '0113': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0114': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0115': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0116': {'designation': 'Business Development Executive', 'department': 'Sales'},
    '0117': {'designation': 'Business Development Executive', 'department': 'Sales'},
}


class Command(BaseCommand):
    help = 'Update employee designations and departments'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all employees with predefined designations',
        )
        parser.add_argument(
            '--id',
            type=str,
            help='Update specific employee by ID (e.g., 0101)',
        )
        parser.add_argument(
            '--designation',
            type=str,
            help='New designation (use with --id)',
        )
        parser.add_argument(
            '--department',
            type=str,
            help='New department (use with --id)',
        )
    
    def handle(self, *args, **options):
        if options['all']:
            self.update_all()
        elif options['id']:
            self.update_single(options['id'], options.get('designation'), options.get('department'))
        else:
            self.stdout.write(
                self.style.ERROR('Please use --all or --id with --designation and --department')
            )
    
    def update_all(self):
        """Update all employees with predefined designations"""
        self.stdout.write(self.style.SUCCESS('Starting employee designation update...'))
        
        updated_count = 0
        not_found_count = 0
        
        for emp_id, data in EMPLOYEE_DESIGNATIONS.items():
            try:
                employee = Employee.objects.get(employee_id=emp_id)
                old_designation = employee.designation
                old_department = employee.department
                
                employee.designation = data['designation']
                employee.department = data['department']
                employee.save()
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {emp_id} - {employee.full_name}\n'
                        f'  Designation: {old_designation} → {data["designation"]}\n'
                        f'  Department: {old_department} → {data["department"]}'
                    )
                )
            except Employee.DoesNotExist:
                not_found_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⊘ Employee {emp_id} not found')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Updated {updated_count} employees successfully!')
        )
        if not_found_count > 0:
            self.stdout.write(
                self.style.WARNING(f'⊘ {not_found_count} employees not found')
            )
    
    def update_single(self, emp_id, designation, department):
        """Update a single employee"""
        if not designation or not department:
            self.stdout.write(
                self.style.ERROR('Both --designation and --department are required')
            )
            return
        
        try:
            employee = Employee.objects.get(employee_id=emp_id)
            old_designation = employee.designation
            old_department = employee.department
            
            employee.designation = designation
            employee.department = department
            employee.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Updated {emp_id} - {employee.full_name}\n'
                    f'  Designation: {old_designation} → {designation}\n'
                    f'  Department: {old_department} → {department}'
                )
            )
        except Employee.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ Employee {emp_id} not found')
            )
