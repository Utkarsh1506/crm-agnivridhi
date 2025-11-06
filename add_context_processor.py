# Quick script to add context processor
import re

settings_file = r'c:\Users\Admin\Desktop\agni\CRM\agnivridhi_crm\settings.py'

with open(settings_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the context processor
old_text = """            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],"""

new_text = """            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'applications.context_processors.pending_applications_count',
            ],"""

if 'applications.context_processors.pending_applications_count' not in content:
    content = content.replace(old_text, new_text)
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Added context processor")
else:
    print("⚠️  Already exists")
