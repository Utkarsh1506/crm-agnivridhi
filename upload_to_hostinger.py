#!/usr/bin/env python3
"""
Automated FTP Upload Script for Hostinger
Uses ftplib to upload project files
"""

import ftplib
import os
from pathlib import Path

# FTP Configuration
FTP_HOST = "195.35.44.250"
FTP_PORT = 65002
FTP_USER = "u623641178"
FTP_PASS = "agnivridhi@CRM121"
REMOTE_DIR = "/public_html/crm.agnivridhiindia.com"

# Local project directory
LOCAL_DIR = r"C:\Users\Admin\Desktop\agni\CRM"

# Files and folders to upload
UPLOAD_FILES = [
    "manage.py",
    "requirements-production.txt",
    "passenger_wsgi.py",
    ".htaccess",
    ".env.production",
    "deploy-hostinger.sh",
    "export_sqlite_data.py",
    "import_to_mysql.py",
]

UPLOAD_FOLDERS = [
    "accounts",
    "agnivridhi_crm",
    "applications",
    "bookings",
    "clients",
    "documents",
    "edit_requests",
    "notifications",
    "payments",
    "schemes",
    "activity_logs",
    "templates",
    "static",
    "media",
]

EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    ".git",
    "venv",
    "db.sqlite3",
    ".env",  # Don't upload local .env
]

def should_exclude(path):
    """Check if path should be excluded"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in str(path):
            return True
    return False

def upload_file(ftp, local_path, remote_path):
    """Upload a single file"""
    try:
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        print(f"✓ Uploaded: {remote_path}")
        return True
    except Exception as e:
        print(f"✗ Failed: {remote_path} - {e}")
        return False

def create_remote_dir(ftp, directory):
    """Create directory on remote server"""
    try:
        ftp.mkd(directory)
        print(f"✓ Created directory: {directory}")
    except:
        pass  # Directory might already exist

def upload_directory(ftp, local_dir, remote_dir):
    """Recursively upload directory"""
    local_path = Path(local_dir)
    
    if not local_path.exists():
        print(f"✗ Local directory not found: {local_dir}")
        return
    
    # Create remote directory
    create_remote_dir(ftp, remote_dir)
    
    # Upload all files in directory
    for item in local_path.iterdir():
        if should_exclude(item):
            continue
            
        remote_item = f"{remote_dir}/{item.name}"
        
        if item.is_file():
            upload_file(ftp, str(item), remote_item)
        elif item.is_dir():
            upload_directory(ftp, str(item), remote_item)

def main():
    print("=" * 60)
    print("Hostinger FTP Upload - Agnivridhi CRM")
    print("=" * 60)
    print()
    
    try:
        # Note: FTP over non-standard port might not work with ftplib
        # SFTP (port 65002) requires paramiko/pysftp instead
        print(f"Connecting to {FTP_HOST}...")
        print("Note: Standard FTP uses port 21, SFTP uses 22")
        print("Your port 65002 suggests SFTP - switching to paramiko...")
        
        # Import paramiko for SFTP
        try:
            import paramiko
        except ImportError:
            print("\n✗ paramiko not installed!")
            print("Run: pip install paramiko")
            print("\nAlternatively, use WinSCP or FileZilla GUI:")
            print(f"  Host: {FTP_HOST}")
            print(f"  Port: {FTP_PORT}")
            print(f"  Protocol: SFTP")
            print(f"  Username: {FTP_USER}")
            print(f"  Password: {FTP_PASS}")
            return
        
        # Connect via SFTP
        transport = paramiko.Transport((FTP_HOST, FTP_PORT))
        transport.connect(username=FTP_USER, password=FTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        print("✓ Connected successfully!")
        print()
        
        # Create base directory
        try:
            sftp.mkdir(REMOTE_DIR)
            print(f"✓ Created: {REMOTE_DIR}")
        except:
            print(f"Directory exists: {REMOTE_DIR}")
        
        sftp.chdir(REMOTE_DIR)
        print(f"✓ Changed to: {REMOTE_DIR}")
        print()
        
        # Upload files
        print("Uploading files...")
        for filename in UPLOAD_FILES:
            local_file = os.path.join(LOCAL_DIR, filename)
            if os.path.exists(local_file):
                sftp.put(local_file, filename)
                print(f"✓ {filename}")
        
        print()
        print("Uploading directories...")
        
        # Upload folders
        for folder in UPLOAD_FOLDERS:
            local_folder = os.path.join(LOCAL_DIR, folder)
            if os.path.exists(local_folder):
                print(f"\nUploading {folder}/...")
                upload_directory_sftp(sftp, local_folder, folder)
        
        sftp.close()
        transport.close()
        
        print()
        print("=" * 60)
        print("✓ Upload Complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. SSH into server: ssh -p 65002 u623641178@195.35.44.250")
        print("2. cd ~/public_html/crm.agnivridhiindia.com")
        print("3. mv .env.production .env")
        print("4. chmod +x deploy-hostinger.sh && ./deploy-hostinger.sh")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease use WinSCP or FileZilla instead:")
        print("Download: https://winscp.net/")

def upload_directory_sftp(sftp, local_dir, remote_dir):
    """Upload directory via SFTP"""
    try:
        sftp.mkdir(remote_dir)
    except:
        pass
    
    for item in os.listdir(local_dir):
        if should_exclude(item):
            continue
            
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"
        
        if os.path.isfile(local_path):
            try:
                sftp.put(local_path, remote_path)
                print(f"  ✓ {remote_path}")
            except Exception as e:
                print(f"  ✗ {remote_path}: {e}")
        elif os.path.isdir(local_path):
            upload_directory_sftp(sftp, local_path, remote_path)

if __name__ == "__main__":
    main()
