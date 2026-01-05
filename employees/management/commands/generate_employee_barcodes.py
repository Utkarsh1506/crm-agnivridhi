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

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate barcodes for all employees (overwrite existing)'
        )

    def handle(self, *args, **options):
        force = options.get('force', False)

        if force:
            qs = Employee.objects.all()
        else:
            # Backfill employees where barcode is null or empty
            qs = Employee.objects.filter(Q(barcode__isnull=True) | Q(barcode=""))
        total = qs.count()
        created = 0
        scope_msg = "(forcing regenerate)" if force else "without barcodes"
        self.stdout.write(self.style.NOTICE(f"Found {total} employees {scope_msg}"))
        for employee in qs:
            try:
                file = EmployeeBarcodeGenerator.generate_barcode(employee.employee_id)
                employee.barcode.save(f"{employee.employee_id}_barcode.png", file, save=True)
                created += 1
                self.stdout.write(self.style.SUCCESS(f"✓ {employee.employee_id} - {employee.full_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ {employee.employee_id}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Done. Generated {created}/{total} barcodes"))
