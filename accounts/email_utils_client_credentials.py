from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_client_credentials_email(client_credential, login_url=None):
    """
    Send client credentials (username, password, login link) to the client via email.
    """
    subject = 'Your Agnivridhi CRM Login Credentials'
    recipient_email = client_credential.email
    if not recipient_email:
        return False

    resolved_login_url = (
        login_url
        or getattr(settings, 'CLIENT_LOGIN_URL', None)
        or getattr(settings, 'LOGIN_URL', '/accounts/login/')
    )

    context = {
        'client': client_credential.client,
        'username': client_credential.username,
        'password': client_credential.plain_password,
        'login_url': resolved_login_url,
    }
    html_message = render_to_string('emails/client_credentials.html', context)
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
        print(f"Error sending client credentials email: {e}")
        return False
