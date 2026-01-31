"""
Clerk Authentication Service
Handles OTP-based email authentication for clients using Clerk
"""
import os
import requests
from django.conf import settings
from django.core.cache import cache
import secrets
import string


class ClerkAuthService:
    """Service to handle Clerk authentication and OTP"""
    
    def __init__(self):
        self.clerk_api_key = os.getenv('CLERK_API_KEY', '')
        self.clerk_api_url = 'https://api.clerk.com/v1'
        self.otp_cache_timeout = 600  # 10 minutes
    
    def send_otp(self, email):
        """
        Send OTP to client email
        Returns: {success: bool, message: str, otp: str (only in dev)}
        """
        try:
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.utils.html import strip_tags
            
            # Generate 6-digit OTP
            otp = ''.join(secrets.choice(string.digits) for _ in range(6))
            
            # Store OTP in cache
            cache_key = f"client_otp_{email}"
            cache.set(cache_key, otp, self.otp_cache_timeout)
            
            # Prepare email content
            subject = 'Your OTP for Agnivridhi CRM Login'
            
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .otp-box {{ background: white; border: 2px solid #667eea; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
                    .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
                    .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Login Verification</h1>
                        <p>Agnivridhi CRM</p>
                    </div>
                    <div class="content">
                        <h2>Hello!</h2>
                        <p>You requested a One-Time Password (OTP) to login to your Agnivridhi CRM account.</p>
                        
                        <div class="otp-box">
                            <p style="margin: 0 0 10px 0; color: #666;">Your verification code is:</p>
                            <div class="otp-code">{otp}</div>
                            <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">Valid for 10 minutes</p>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Security Notice:</strong>
                            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                                <li>Never share this OTP with anyone</li>
                                <li>Agnivridhi staff will never ask for your OTP</li>
                                <li>This code expires in 10 minutes</li>
                            </ul>
                        </div>
                        
                        <p>If you didn't request this code, please ignore this email or contact support if you have concerns.</p>
                    </div>
                    <div class="footer">
                        <p>© 2026 Agnivridhi India. All rights reserved.</p>
                        <p>This is an automated message, please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            plain_message = f"""
            Your OTP for Agnivridhi CRM Login
            
            Hello!
            
            You requested a One-Time Password (OTP) to login to your Agnivridhi CRM account.
            
            Your verification code is: {otp}
            
            This code is valid for 10 minutes.
            
            Security Notice:
            - Never share this OTP with anyone
            - Agnivridhi staff will never ask for your OTP
            - This code expires in 10 minutes
            
            If you didn't request this code, please ignore this email.
            
            © 2026 Agnivridhi India. All rights reserved.
            """
            
            # Send email
            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as email_error:
                # Log the specific email error
                print(f"[EMAIL ERROR] SMTP failed for {email}: {str(email_error)}")
                # Still return success with OTP cached (for development/testing)
                # In production, you might want to fail completely
                if settings.DEBUG:
                    print(f"[DEBUG] OTP cached anyway: {otp}")
                    return {
                        'success': True,
                        'message': f'OTP generated (email may fail): {otp}',
                        'otp': otp
                    }
                else:
                    raise  # Re-raise in production to trigger outer exception handler
            
            # Also log for debugging (only in DEBUG mode)
            if settings.DEBUG:
                print(f"[SUCCESS] OTP sent to {email}: {otp}")
            
            return {
                'success': True,
                'message': f'OTP sent to {email}',
                'otp': otp if settings.DEBUG else None  # Only return OTP in debug
            }
        except Exception as e:
            # Log the error for debugging
            import traceback
            print(f"[ERROR] Failed to send OTP to {email}: {str(e)}")
            print(f"[TRACEBACK] {traceback.format_exc()}")
            return {
                'success': False,
                'message': str(e),
                'otp': None
            }
    
    def verify_otp(self, email, otp):
        """
        Verify OTP provided by client
        Returns: {success: bool, message: str, is_valid: bool}
        """
        try:
            cache_key = f"client_otp_{email}"
            stored_otp = cache.get(cache_key)
            
            if not stored_otp:
                return {
                    'success': False,
                    'message': 'OTP expired. Please request a new one.',
                    'is_valid': False
                }
            
            if str(otp) == str(stored_otp):
                # Clear OTP after successful verification
                cache.delete(cache_key)
                return {
                    'success': True,
                    'message': 'OTP verified successfully',
                    'is_valid': True
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid OTP. Please try again.',
                    'is_valid': False
                }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'is_valid': False
            }
    
    def create_client_session(self, email, client):
        """
        Create authenticated session for client after OTP verification
        Returns: {success: bool, token: str}
        """
        try:
            from django.contrib.auth import authenticate
            from rest_framework.authtoken.models import Token
            
            # Get or create token for the client's user
            user = client.user
            token, created = Token.objects.get_or_create(user=user)
            
            return {
                'success': True,
                'token': token.key,
                'user_id': user.id,
                'client_id': client.id
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'token': None
            }


# Initialize service
clerk_service = ClerkAuthService()
