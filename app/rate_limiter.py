"""
Rate limiter configuration for the Career Guidance API.
Centralized rate limiter instance to avoid circular imports.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Create shared rate limiter instance
limiter = Limiter(key_func=get_remote_address) 