"""
Employee module utilities.
Helper functions for IP detection, validation, etc.
"""
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Get client IP address from request.
    Handles proxy scenarios (X-Forwarded-For, X-Real-IP headers).
    
    Args:
        request: Django request object
        
    Returns:
        str: Client IP address
    """
    # Check X-Forwarded-For header (for proxies/load balancers)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, get the first one
        ip = x_forwarded_for.split(',')[0].strip()
        return ip
    
    # Check X-Real-IP header
    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    if x_real_ip:
        return x_real_ip
    
    # Fall back to REMOTE_ADDR
    return request.META.get('REMOTE_ADDR', '0.0.0.0')
