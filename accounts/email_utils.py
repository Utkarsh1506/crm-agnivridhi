"""
Email notification utilities for Agnivridhi CRM
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_payment_approval_email(payment, approved_by):
    """Send email notification when payment is approved"""
    subject = f'Payment Approved - ₹{payment.amount} for {payment.client.company_name}'
    
    # Get recipient email
    recipient_email = None
    if payment.received_by and payment.received_by.email:
        recipient_email = payment.received_by.email
    
    if not recipient_email:
        return False
    
    context = {
        'payment': payment,
        'approved_by': approved_by,
        'client': payment.client,
        'booking': payment.booking,
    }
    
    # Render HTML email
    html_message = render_to_string('emails/payment_approved.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_payment_rejection_email(payment, rejected_by, reason=None):
    """Send email notification when payment is rejected"""
    subject = f'Payment Rejected - ₹{payment.amount} for {payment.client.company_name}'
    
    recipient_email = None
    if payment.received_by and payment.received_by.email:
        recipient_email = payment.received_by.email
    
    if not recipient_email:
        return False
    
    context = {
        'payment': payment,
        'rejected_by': rejected_by,
        'client': payment.client,
        'booking': payment.booking,
        'reason': reason,
    }
    
    html_message = render_to_string('emails/payment_rejected.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_booking_confirmation_email(booking):
    """Send booking confirmation email to client"""
    subject = f'Booking Confirmation - {booking.booking_id}'
    
    # Try to get client email
    recipient_email = None
    if hasattr(booking.client, 'contact_email') and booking.client.contact_email:
        recipient_email = booking.client.contact_email
    elif hasattr(booking.client, 'user') and booking.client.user and booking.client.user.email:
        recipient_email = booking.client.user.email
    
    if not recipient_email:
        return False
    
    context = {
        'booking': booking,
        'client': booking.client,
        'service': booking.service,
    }
    
    html_message = render_to_string('emails/booking_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_application_status_email(application):
    """Send email when application status changes"""
    subject = f'Application Status Update - {application.application_id}'
    
    recipient_email = None
    if hasattr(application.client, 'contact_email') and application.client.contact_email:
        recipient_email = application.client.contact_email
    elif hasattr(application.client, 'user') and application.client.user and application.client.user.email:
        recipient_email = application.client.user.email
    
    if not recipient_email:
        return False
    
    context = {
        'application': application,
        'client': application.client,
        'scheme': application.scheme,
        'status': application.get_status_display(),
    }
    
    html_message = render_to_string('emails/application_status.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_welcome_email(user):
    """Send welcome email to new users"""
    subject = 'Welcome to Agnivridhi CRM'
    
    if not user.email:
        return False
    
    context = {
        'user': user,
        'role': user.get_role_display() if hasattr(user, 'get_role_display') else 'User',
    }
    
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
