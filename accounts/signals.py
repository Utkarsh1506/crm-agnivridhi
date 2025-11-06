"""
Django signals for accounts app.

Handles automated actions on user events:
- Reset user session when role changes (force re-login for security)
- Log role changes for audit trail
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from .models import User
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=User)
def reset_session_on_role_change(sender, instance, **kwargs):
    """
    Reset user session when role changes to enforce access control.
    
    Security rationale:
    - When an admin changes a user's role, their active session may still
      have cached permissions or navigation state from the old role
    - Forcing re-login ensures they get the correct dashboard and permissions
    - Prevents privilege escalation if role is downgraded
    
    Implementation:
    - Clears last_login to trigger Django's session invalidation
    - User will be prompted to log in again on next request
    """
    if instance.pk:  # Only for existing users (not new signups)
        try:
            old_user = User.objects.get(pk=instance.pk)
            
            # Check if role has changed
            if old_user.role != instance.role:
                logger.info(
                    f"Role change detected for user {instance.username}: "
                    f"{old_user.role} → {instance.role}. Session will be reset."
                )
                
                # Clear last_login to force re-authentication
                instance.last_login = None
                
                # Optional: Delete all active sessions for this user
                # This ensures immediate logout even if they're currently logged in
                try:
                    sessions = Session.objects.all()
                    for session in sessions:
                        session_data = session.get_decoded()
                        if session_data.get('_auth_user_id') == str(instance.pk):
                            session.delete()
                            logger.info(f"Deleted active session for user {instance.username}")
                except Exception as e:
                    logger.warning(f"Could not delete sessions for user {instance.username}: {e}")
        
        except User.DoesNotExist:
            # This shouldn't happen, but handle gracefully
            pass
        except Exception as e:
            logger.error(f"Error in reset_session_on_role_change: {e}")


@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    """
    Log user creation events for audit trail.
    
    Helpful for:
    - Security audits
    - Compliance tracking
    - Onboarding analytics
    """
    if created:
        logger.info(
            f"New user created: {instance.username} "
            f"(Role: {instance.get_role_display()}, Email: {instance.email})"
        )
