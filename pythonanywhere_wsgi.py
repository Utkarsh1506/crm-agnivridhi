"""
WSGI Configuration for PythonAnywhere
======================================

Copy this entire file contents to your WSGI configuration file in PythonAnywhere.

To find it:
1. Go to PythonAnywhere "Web" tab
2. Look for "Code" section
3. Click on the WSGI configuration file link
4. Replace ALL contents with this file
5. Update 'agnivridhi' to YOUR PythonAnywhere username
6. Save and reload your web app
"""

import os
import sys

# ========================================
# IMPORTANT: Replace 'agnivridhi' with YOUR PythonAnywhere username
# ========================================
USERNAME = 'agnivridhi'  # <-- CHANGE THIS
PROJECT_NAME = 'crm-agnivridhi'

# Add your project directory to the sys.path
project_path = f'/home/{USERNAME}/{PROJECT_NAME}'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'agnivridhi_crm.settings'

# Load environment variables from .env file
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(f'/home/{USERNAME}/{PROJECT_NAME}/.env')
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ Loaded environment from: {env_path}")
else:
    print(f"⚠ WARNING: .env file not found at {env_path}")

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

print("✓ Django WSGI application initialized successfully")
