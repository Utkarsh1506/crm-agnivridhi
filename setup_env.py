"""
Environment Setup Helper
Helps create .env file with proper configuration
"""

import os
import secrets
import string

def generate_secret_key(length=50):
    """Generate a strong Django SECRET_KEY"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_env_file():
    """Create .env file from .env.example"""
    print("=" * 60)
    print("🔧 AGNIVRIDHI CRM - Environment Setup")
    print("=" * 60)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("\n⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborted.")
            return
    
    # Check if .env.example exists
    if not os.path.exists('.env.example'):
        print("\n❌ .env.example file not found!")
        return
    
    print("\n📝 Creating .env file...")
    
    # Generate SECRET_KEY
    secret_key = generate_secret_key()
    print(f"  ✅ Generated SECRET_KEY: {secret_key[:20]}...")
    
    # Read .env.example
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Replace SECRET_KEY placeholder
    content = content.replace(
        'SECRET_KEY=your-secret-key-here-generate-using-django',
        f'SECRET_KEY={secret_key}'
    )
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(content)
    
    print("  ✅ .env file created successfully!")
    
    print("\n" + "=" * 60)
    print("📋 NEXT STEPS - Configure the following in .env:")
    print("=" * 60)
    
    print("\n1️⃣  Email Configuration (Required)")
    print("   Open .env and set:")
    print("   - EMAIL_HOST_USER=your_email@gmail.com")
    print("   - EMAIL_HOST_PASSWORD=your_16_char_app_password")
    print("\n   📖 Get Gmail App Password:")
    print("      https://support.google.com/accounts/answer/185833")
    
    print("\n2️⃣  Twilio WhatsApp (Optional)")
    print("   Open .env and set:")
    print("   - TWILIO_ACCOUNT_SID=ACxxxxxxxxx")
    print("   - TWILIO_AUTH_TOKEN=your_token")
    print("\n   📖 Get Twilio credentials:")
    print("      https://console.twilio.com/")
    
    print("\n3️⃣  Test Configuration")
    print("   Run: python test_system.py")
    
    print("\n4️⃣  Start Development Server")
    print("   Run: python manage.py runserver")
    
    print("\n" + "=" * 60)
    print("✅ Setup complete! Edit .env file now.")
    print("=" * 60)


if __name__ == '__main__':
    try:
        create_env_file()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
