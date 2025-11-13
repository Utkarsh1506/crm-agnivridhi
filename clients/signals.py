from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Client, ClientCredential
import secrets
import string

User = get_user_model()


@receiver(post_save, sender=Client)
def create_client_credentials(sender, instance, created, **kwargs):
    """
    Auto-generate login credentials when a new client is created AND approved.
    For sales-created clients, credentials are generated only after manager approval.
    """
    # Only generate credentials if:
    # 1. Client is newly created OR just got approved
    # 2. Client has a user account
    # 3. Client is approved
    # 4. Credentials don't already exist
    
    if instance.user and instance.is_approved:
        # Check if credentials already exist
        if not ClientCredential.objects.filter(client=instance).exists():
            # Generate a secure random password
            password_length = 12
            characters = string.ascii_letters + string.digits + "@#$%"
            plain_password = ''.join(secrets.choice(characters) for _ in range(password_length))
            
            # Set the password for the user
            instance.user.set_password(plain_password)
            instance.user.save()
            
            # Store credentials for admin/owner to view
            ClientCredential.objects.create(
                client=instance,
                username=instance.user.username,
                email=instance.user.email,
                plain_password=plain_password,
                created_by=instance.created_by
            )
