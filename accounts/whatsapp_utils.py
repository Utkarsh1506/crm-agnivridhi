"""
WhatsApp notification utilities for Agnivridhi CRM
Uses Twilio WhatsApp Cloud API

Setup Instructions:
1. Sign up for Twilio account: https://www.twilio.com/try-twilio
2. Get WhatsApp sandbox or approved template: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
3. Add credentials to .env:
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886  # Sandbox number

For production:
- Apply for WhatsApp Business API approval
- Create message templates
- Get your production WhatsApp number
"""

from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging

logger = logging.getLogger(__name__)


def get_twilio_client():
    """Initialize and return Twilio client"""
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        logger.warning("Twilio credentials not configured. WhatsApp notifications disabled.")
        return None
    
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        return client
    except Exception as e:
        logger.error(f"Error initializing Twilio client: {e}")
        return None


def send_whatsapp_message(to_number, message):
    """
    Send WhatsApp message via Twilio
    
    Args:
        to_number (str): Recipient phone number with country code (e.g., +919876543210)
        message (str): Message content
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    client = get_twilio_client()
    if not client:
        logger.warning(f"Cannot send WhatsApp to {to_number}: Twilio client not configured")
        return False
    
    try:
        # Ensure number has whatsapp: prefix
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            body=message,
            to=to_number
        )
        
        logger.info(f"WhatsApp sent successfully. SID: {message.sid}")
        return True
        
    except TwilioRestException as e:
        logger.error(f"Twilio error sending WhatsApp to {to_number}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending WhatsApp to {to_number}: {e}")
        return False


def send_payment_approval_whatsapp(payment):
    """Send WhatsApp notification for payment approval"""
    if not payment.client.contact_phone:
        logger.warning(f"No phone number for client {payment.client.company_name}")
        return False
    
    message = f"""
✅ *Payment Approved - Agnivridhi India*

Dear {payment.client.contact_name},

Your payment has been approved!

*Payment Details:*
Amount: ₹{payment.amount}
Method: {payment.get_payment_method_display()}
Reference: {payment.reference_id or 'N/A'}
Date: {payment.payment_date.strftime('%d %b %Y')}

Thank you for your business!

- Agnivridhi India Team
    """.strip()
    
    return send_whatsapp_message(payment.client.contact_phone, message)


def send_payment_rejection_whatsapp(payment, reason=''):
    """Send WhatsApp notification for payment rejection"""
    if not payment.client.contact_phone:
        logger.warning(f"No phone number for client {payment.client.company_name}")
        return False
    
    message = f"""
❌ *Payment Issue - Agnivridhi India*

Dear {payment.client.contact_name},

Your payment requires attention.

*Payment Details:*
Amount: ₹{payment.amount}
Reference: {payment.reference_id or 'N/A'}
Status: Requires Review

{f'Reason: {reason}' if reason else ''}

Please contact us for clarification.

- Agnivridhi India Team
    """.strip()
    
    return send_whatsapp_message(payment.client.contact_phone, message)


def send_booking_confirmation_whatsapp(booking):
    """Send WhatsApp notification for booking confirmation"""
    if not booking.client.contact_phone:
        logger.warning(f"No phone number for client {booking.client.company_name}")
        return False
    
    message = f"""
📅 *Booking Confirmed - Agnivridhi India*

Dear {booking.client.contact_name},

Your booking has been confirmed!

*Booking Details:*
Service: {booking.service.name}
Amount: ₹{booking.amount}
Date: {booking.booking_date.strftime('%d %b %Y')}
Booking ID: {booking.id}

We look forward to serving you!

- Agnivridhi India Team
    """.strip()
    
    return send_whatsapp_message(booking.client.contact_phone, message)


def send_application_status_whatsapp(application):
    """Send WhatsApp notification for application status update"""
    if not application.client.contact_phone:
        logger.warning(f"No phone number for client {application.client.company_name}")
        return False
    
    status_emoji = {
        'PENDING': '⏳',
        'UNDER_REVIEW': '🔍',
        'APPROVED': '✅',
        'REJECTED': '❌',
        'ON_HOLD': '⏸️'
    }
    
    emoji = status_emoji.get(application.status, '📋')
    
    message = f"""
{emoji} *Application Update - Agnivridhi India*

Dear {application.client.contact_name},

Your application status has been updated.

*Application Details:*
Scheme: {application.scheme.name}
Status: {application.get_status_display()}
Amount Requested: ₹{application.amount_requested or 'N/A'}
{f'Amount Approved: ₹{application.amount_approved}' if application.amount_approved else ''}

{f'Note: {application.rejection_reason}' if application.rejection_reason else ''}

For queries, please contact us.

- Agnivridhi India Team
    """.strip()
    
    return send_whatsapp_message(application.client.contact_phone, message)


def send_custom_whatsapp(phone_number, message_text):
    """
    Send custom WhatsApp message
    Can be used from admin panel or API
    
    Args:
        phone_number (str): Phone number with country code
        message_text (str): Custom message content
    
    Returns:
        bool: True if sent successfully
    """
    return send_whatsapp_message(phone_number, message_text)
