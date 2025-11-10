import sys
import os

# IMPORTANT: Update these paths to match your Hostinger account
# For subdomain: crm.agnivridhiindia.com
INTERP = "/home/u623641178/public_html/crm.agnivridhiindia.com/venv/bin/python"
VIRTUALENV = "/home/u623641178/public_html/crm.agnivridhiindia.com/venv"
PROJECT_ROOT = "/home/u623641178/public_html/crm.agnivridhiindia.com"

# Add your project directory to the sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Activate virtual environment
if os.path.exists(INTERP):
    os.environ['PYTHON'] = INTERP
    
# Alternative way to activate venv
activate_this = os.path.join(VIRTUALENV, 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec(code, dict(__file__=activate_this))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agnivridhi_crm.settings')

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
