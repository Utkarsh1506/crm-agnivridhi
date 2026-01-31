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
            # Generate 6-digit OTP
            otp = ''.join(secrets.choice(string.digits) for _ in range(6))
            
            # Store OTP in cache
            cache_key = f"client_otp_{email}"
            cache.set(cache_key, otp, self.otp_cache_timeout)
            
            # In production, send via email service
            # For now, log it
            print(f"OTP for {email}: {otp}")
            
            return {
                'success': True,
                'message': f'OTP sent to {email}',
                'otp': otp if settings.DEBUG else None  # Only return OTP in debug
            }
        except Exception as e:
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
