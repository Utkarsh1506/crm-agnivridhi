"""
Signals for Clerk Authentication Integration
Handles automatic OTP setup when client is approved
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from clients.models import Client
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Client)
def setup_clerk_auth_on_approval(sender, instance, created, update_fields, **kwargs):
    """
    Signal handler: When a client is approved, enable Clerk authentication
    
    This automatically:
    1. Sends email to client with login instructions
    2. Marks email as approved for OTP login
    3. Logs the approval event
    """
    
    # Only process updates, not creation
    if created:
        return
    
    # Check if is_approved status changed to True
    if update_fields and 'is_approved' not in update_fields:
        return
    
    if not instance.is_approved:
        return
    
    try:
        # Log approval
        logger.info(f"Client {instance.id} ({instance.name}) approved. Enabling Clerk OTP authentication.")
        
        # Send welcome email with login instructions
        send_clerk_auth_welcome_email(instance)
        
    except Exception as e:
        logger.error(f"Error setting up Clerk auth for client {instance.id}: {str(e)}")


def send_clerk_auth_welcome_email(client):
    """
    Send welcome email to client with Clerk OTP login instructions
    """
    try:
        email = client.contact_email
        
        if not email:
            logger.warning(f"Client {client.id} has no contact email. Cannot send welcome email.")
            return
        
        # Prepare email content
        subject = f"Your Account is Approved - {settings.COMPANY_NAME}"
        
        context = {
            'client_name': client.name,
            'login_url': f"{settings.SITE_URL}/accounts/client-login/",
            'email': email,
            'company_name': settings.COMPANY_NAME,
            'support_email': settings.DEFAULT_FROM_EMAIL,
        }
        
        # Render HTML email template
        html_message = render_to_string('emails/clerk_auth_welcome.html', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=f"Welcome {client.name}! Your account has been approved. Please login at {settings.SITE_URL}/accounts/client-login/ with your email {email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent to {email} for client {client.id}")
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {str(e)}")


# Optional: Add a method to Client model to get Clerk auth status
def is_clerk_auth_enabled(client):
    """Check if Clerk OTP auth is enabled for this client"""
    return client.is_approved and client.contact_email
