"""
Update settings.py to add pending_applications_count context processor
Run this script once to update settings
"""
import re

settings_path = r"c:\Users\Admin\Desktop\agni\CRM\agnivridhi_crm\settings.py"

with open(settings_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add context processor after messages
old_pattern = r"'django\.contrib\.messages\.context_processors\.messages',\n            \],"
new_pattern = "'django.contrib.messages.context_processors.messages',\n                'applications.context_processors.pending_applications_count',\n            ],"

if 'applications.context_processors.pending_applications_count' not in content:
    content = re.sub(old_pattern, new_pattern, content)
    
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added context processor to settings.py")
else:
    print("⚠️  Context processor already exists")
