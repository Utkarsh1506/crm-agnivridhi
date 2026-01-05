"""
Employees app configuration.
Manages Employee Identity & Verification System.
"""
from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees'
    verbose_name = 'Employee Verification System'
    
    def ready(self):
        """Register signal handlers when app is ready."""
        import employees.signals  # noqa

