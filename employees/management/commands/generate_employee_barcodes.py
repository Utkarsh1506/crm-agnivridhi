"""
Generate barcodes for employees missing them.
Usage:
    python manage.py generate_employee_barcodes
"""
from django.core.management.base import BaseCommand
from django.db.models import Q
from employees.models import Employee
from employees.barcode_utils import EmployeeBarcodeGenerator


class Command(BaseCommand):
    help = "Generate barcodes for all employees missing one"

    def handle(self, *args, **options):
        # Backfill employees where barcode is null or empty
        qs = Employee.objects.filter(Q(barcode__isnull=True) | Q(barcode=""))
        total = qs.count()
        created = 0
        self.stdout.write(self.style.NOTICE(f"Found {total} employees without barcodes"))
        for employee in qs:
            try:
                file = EmployeeBarcodeGenerator.generate_barcode(employee.employee_id)
                employee.barcode.save(f"{employee.employee_id}_barcode.png", file, save=True)
                created += 1
                self.stdout.write(self.style.SUCCESS(f"✓ {employee.employee_id} - {employee.full_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ {employee.employee_id}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Done. Generated {created}/{total} barcodes"))
