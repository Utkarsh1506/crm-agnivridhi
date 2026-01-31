"""
Clerk Authentication Service for OTP
Handles OTP-based email authentication using Clerk REST API
Uses requests library instead of SDK to avoid dependency issues on PythonAnywhere
"""
import os
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class ClerkOTPService:
    """Service to handle Clerk-based OTP authentication via REST API"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Get API key from environment or settings (will try multiple sources)
        # This pattern handles PythonAnywhere where .env might not exist initially
        self.clerk_api_key = os.getenv('CLERK_SECRET_KEY') or getattr(settings, 'CLERK_SECRET_KEY', '')
        
        if not self.clerk_api_key or self.clerk_api_key == '':
            logger.warning("⚠️ CLERK_SECRET_KEY not configured at initialization - will attempt to load from environment at runtime")
            # Don't fail here - keys might be loaded later from PythonAnywhere environment
            self.clerk_api_key = ''
        
        self.api_base = 'https://api.clerk.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.clerk_api_key}' if self.clerk_api_key else 'Bearer ',
            'Content-Type': 'application/json'
        }
        
        if self.clerk_api_key:
            logger.info(f"✅ ClerkOTPService initialized successfully - API key loaded (length: {len(self.clerk_api_key)})")
        else:
            logger.warning(f"⚠️ ClerkOTPService initialized but CLERK_SECRET_KEY is empty - service will fail until configured")
        
        self._initialized = True
    
    def send_otp(self, email):
        """
        Send OTP to client email via Clerk REST API
        Returns: {success: bool, message: str, sign_in_id: str}
        """
        # Refresh API key in case environment changed (handles PythonAnywhere env var loading)
        self.clerk_api_key = os.getenv('CLERK_SECRET_KEY') or getattr(settings, 'CLERK_SECRET_KEY', '')
        
        if not self.clerk_api_key:
            logger.error("❌ CLERK_SECRET_KEY is empty at send_otp time - environment variables not configured")
            logger.error(f"   Expected in: environment variables or settings.CLERK_SECRET_KEY")
            logger.error(f"   This typically means .env file is missing or environment variables not set on PythonAnywhere")
            return {
                'success': False,
                'message': 'OTP service not configured. Please contact support.',
                'sign_in_id': None,
                'otp': None
            }
        
        # Update headers with fresh key
        self.headers['Authorization'] = f'Bearer {self.clerk_api_key}'
        
        try:
            logger.info(f"📧 Sending OTP to {email} via Clerk API")
            
            # Create sign-in attempt with email code strategy
            # Clerk automatically sends the OTP code to the email
            response = requests.post(
                f'{self.api_base}/sign_ins',
                headers=self.headers,
                json={
                    'strategy': 'email_code',
                    'identifier': email
                },
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                sign_in_id = data.get('id')
                logger.info(f"✅ OTP sent successfully to {email}, sign_in_id: {sign_in_id}")
                
                return {
                    'success': True,
                    'message': f'OTP sent to {email}. Please check your inbox.',
                    'sign_in_id': sign_in_id,
                    'otp': None  # Clerk doesn't return OTP for security
                }
            else:
                error_msg = response.text
                logger.error(f"❌ Clerk API error (status {response.status_code}): {error_msg}")
                return {
                    'success': False,
                    'message': f'Failed to send OTP: {response.status_code}',
                    'sign_in_id': None,
                    'otp': None
                }
        
        except requests.RequestException as e:
            logger.error(f"❌ Request error sending OTP to {email}: {str(e)}", exc_info=True)
            logger.error(f"   This might mean Clerk API is unreachable from your location")
            return {
                'success': False,
                'message': f'Failed to send OTP: Network error',
                'sign_in_id': None,
                'otp': None
            }
        
        except Exception as e:
            logger.error(f"❌ Unexpected error sending OTP to {email}: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': 'An unexpected error occurred. Please try again.',
                'sign_in_id': None,
                'otp': None
            }
    
    def verify_otp(self, sign_in_id, otp_code):
        """
        Verify OTP code via Clerk REST API
        Returns: {success: bool, message: str, is_valid: bool, user_id: str}
        """
        # Refresh API key in case environment changed
        self.clerk_api_key = os.getenv('CLERK_SECRET_KEY') or getattr(settings, 'CLERK_SECRET_KEY', '')
        
        if not self.clerk_api_key:
            logger.error("❌ CLERK_SECRET_KEY is empty at verify_otp time - environment variables not configured")
            return {
                'success': False,
                'message': 'OTP service not configured',
                'is_valid': False,
                'user_id': None,
                'session_id': None
            }
        
        # Update headers with fresh key
        self.headers['Authorization'] = f'Bearer {self.clerk_api_key}'
        
        try:
            logger.info(f"🔐 Verifying OTP for sign-in: {sign_in_id}")
            
            # Verify the OTP code via Clerk API
            response = requests.patch(
                f'{self.api_base}/sign_ins/{sign_in_id}/attempt_verification',
                headers=self.headers,
                json={
                    'code': otp_code,
                    'strategy': 'email_code'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                
                if status == 'complete':
                    user_id = data.get('created_user_id')
                    session_id = data.get('created_session_id')
                    logger.info(f"✅ OTP verified successfully, user_id: {user_id}")
                    
                    return {
                        'success': True,
                        'message': 'OTP verified successfully',
                        'is_valid': True,
                        'user_id': user_id,
                        'session_id': session_id
                    }
                else:
                    logger.warning(f"⚠️ OTP verification incomplete, status: {status}")
                    return {
                        'success': False,
                        'message': 'OTP verification failed. Please try again.',
                        'is_valid': False,
                        'user_id': None,
                        'session_id': None
                    }
            else:
                error_msg = response.text
                logger.error(f"❌ Clerk API error (status {response.status_code}): {error_msg}")
                return {
                    'success': False,
                    'message': 'Invalid OTP code',
                    'is_valid': False,
                    'user_id': None,
                    'session_id': None
                }
        
        except requests.RequestException as e:
            logger.error(f"❌ Request error verifying OTP: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': 'Verification failed: Network error',
                'is_valid': False,
                'user_id': None,
                'session_id': None
            }
        
        except Exception as e:
            logger.error(f"Unexpected error verifying OTP: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': 'Verification failed. Please try again.',
                'is_valid': False,
                'user_id': None,
                'session_id': None
            }
    
    def get_or_create_user(self, clerk_user_id, email):
        """
        Get Clerk user details and sync with Django user
        Returns: {success: bool, user: User, django_user: User}
        """
        if not self.clerk_api_key:
            logger.error("CLERK_SECRET_KEY not configured")
            return {
                'success': False,
                'clerk_user': None,
                'django_user': None,
                'error': 'OTP service not configured'
            }
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            logger.info(f"Getting or creating user for clerk_user_id: {clerk_user_id}, email: {email}")
            
            # Get user from Clerk
            response = requests.get(
                f'{self.api_base}/users/{clerk_user_id}',
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch Clerk user: {response.status_code}")
                return {
                    'success': False,
                    'clerk_user': None,
                    'django_user': None,
                    'error': f'Failed to fetch user: {response.status_code}'
                }
            
            clerk_user = response.json()
            logger.info(f"Retrieved Clerk user: {clerk_user_id}")
            
            # Get or create Django user (for backward compatibility)
            django_user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'is_active': True,
                }
            )
            
            if created:
                logger.info(f"Created Django user: {django_user.username}")
            else:
                logger.info(f"Found existing Django user: {django_user.username}")
            
            return {
                'success': True,
                'clerk_user': clerk_user,
                'django_user': django_user
            }
        
        except requests.RequestException as e:
            logger.error(f"Request error getting user: {str(e)}", exc_info=True)
            return {
                'success': False,
                'clerk_user': None,
                'django_user': None,
                'error': str(e)
            }
        
        except Exception as e:
            logger.error(f"Unexpected error getting user: {str(e)}", exc_info=True)
            return {
                'success': False,
                'clerk_user': None,
                'django_user': None,
                'error': str(e)
            }


# Lazy initialization function - creates service on first access
def get_clerk_service():
    """Get or create the Clerk OTP service instance"""
    global clerk_service
    if clerk_service is None:
        try:
            clerk_service = ClerkOTPService()
        except Exception as e:
            logger.error(f"Failed to initialize Clerk service: {str(e)}")
            clerk_service = ClerkOTPService()  # Create with empty key
    return clerk_service


# Initialize as None - will be created on first use
clerk_service = None

# Create initial instance for backward compatibility
try:
    clerk_service = ClerkOTPService()
except Exception as e:
    logger.warning(f"Clerk service initialization warning: {str(e)}")
    clerk_service = ClerkOTPService()
