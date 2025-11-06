from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import resolve, Resolver404
from django.http import HttpResponseForbidden
import re

def _get_site_settings():
    try:
        from .models import SiteSettings
        return SiteSettings.get()
    except Exception:
        return None


class RoleAccessMiddleware:
    """
    Middleware to restrict access to URL namespaces based on user role.
    
    Security Model:
    - Each user role has an allowlist of namespaces (see ROLE_NAMESPACE_MAP in constants)
    - Requests to disallowed namespaces return 403 Forbidden
    - Unauthenticated users are redirected to login (except exempt patterns)
    - Superusers bypass all namespace checks
    
    Placement: Must come after AuthenticationMiddleware in MIDDLEWARE setting
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Import here to avoid circular imports
        from .constants import ROLE_NAMESPACE_MAP, EXEMPT_URL_PATTERNS
        self.role_namespace_map = ROLE_NAMESPACE_MAP
        self.exempt_patterns = EXEMPT_URL_PATTERNS
    
    def __call__(self, request):
        # Check if URL should bypass middleware
        if self._is_exempt_url(request.path):
            return self.get_response(request)
        
        # Allow unauthenticated access to pass through (login view will handle)
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Superusers can access everything
        if request.user.is_superuser:
            return self.get_response(request)
        
        try:
            # Resolve current URL to namespace
            resolver_match = resolve(request.path)
            namespace = resolver_match.namespace
            
            # If no namespace, allow (could be root, error pages, etc.)
            if not namespace:
                return self.get_response(request)
            
            # Get allowed namespaces for user's role
            user_role = request.user.normalized_role
            allowed_namespaces = self.role_namespace_map.get(user_role, [])
            
            # Check if namespace is allowed
            if namespace not in allowed_namespaces:
                messages.error(
                    request,
                    f"Unauthorized: You cannot access the '{namespace}' section with your current role."
                )
                return HttpResponseForbidden(
                    f"<h2>403 - Access Denied</h2>"
                    f"<p>Your role ({user_role}) doesn't have permission to access this section.</p>"
                    f"<p><a href='/dashboard/'>Return to Dashboard</a></p>"
                )
        
        except Resolver404:
            # URL doesn't exist, let Django handle it (will raise 404)
            pass
        except Exception as e:
            # Log unexpected errors but don't block request
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"RoleAccessMiddleware error: {e}")
        
        return self.get_response(request)
    
    def _is_exempt_url(self, path):
        """Check if URL pattern should bypass middleware checks"""
        for pattern in self.exempt_patterns:
            if re.match(pattern, path):
                return True
        return False


class SessionIdleTimeoutMiddleware:
    """Middleware to log out users after SESSION_IDLE_TIMEOUT seconds of inactivity.

    It stores the last activity timestamp in the session under '_last_activity'.
    If SESSION_IDLE_TIMEOUT is 0 or not set, the middleware is a no-op.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = getattr(settings, 'SESSION_IDLE_TIMEOUT', 0)

    def __call__(self, request):
        # Determine effective idle timeout from DB settings or fallback to Django settings
        effective_idle_timeout = self.timeout
        site_settings = _get_site_settings()
        if site_settings and getattr(site_settings, 'session_idle_timeout', None) is not None:
            effective_idle_timeout = int(site_settings.session_idle_timeout or 0)

        # Per-request session expiry based on site settings
        user = getattr(request, 'user', None)
        if user is not None and getattr(user, 'is_authenticated', False) and site_settings:
            try:
                if site_settings.session_expire_at_browser_close:
                    # 0 means expire at browser close
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(int(site_settings.session_cookie_age or 0))
            except Exception:
                pass

        # Only act for authenticated users and when timeout > 0
        if user is not None and getattr(user, 'is_authenticated', False) and effective_idle_timeout and request.method != 'OPTIONS':
            now = timezone.now().timestamp()
            last_activity = request.session.get('_last_activity')
            if last_activity:
                try:
                    last = float(last_activity)
                except Exception:
                    last = now
                elapsed = now - last
                if elapsed > effective_idle_timeout:
                    # Timeout expired: log user out and redirect to login
                    logout(request)
                    request.session.flush()
                    messages.warning(request, 'You have been logged out due to inactivity. Please log in again.')
                    return redirect('accounts:login')
            # Update last activity
            request.session['_last_activity'] = now

        response = self.get_response(request)
        return response
