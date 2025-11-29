import os
import sys

USERNAME = 'agnivridhicrm'  # Your PythonAnywhere username
PROJECT_NAME = 'crm-agnivridhi'

# Fix: Use the variable you defined (project_path instead of path)
project_path = f'/home/{USERNAME}/{PROJECT_NAME}'
if project_path not in sys.path:
    sys.path.append(project_path)

# Set environment variables BEFORE importing Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'agnivridhi_crm.settings'

# Email Configuration overrides DISABLED
# Let Django use defaults from agnivridhi_crm/settings.py
# If needed later, re-enable a provider block below.
#
# Example: Hostinger (from settings.py)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.hostinger.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'noreply@agnivridhiindia.com'
# EMAIL_HOST_PASSWORD = 'NoReply@121'
# DEFAULT_FROM_EMAIL = 'Agnivridhi CRM <noreply@agnivridhiindia.com>'

# Optional: Load .env file if it exists
from pathlib import Path
env_path = Path(f'/home/{USERNAME}/{PROJECT_NAME}/.env')
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
