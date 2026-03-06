"""
============================================================================
Authentication Module
============================================================================
Microsoft 365 / Azure AD authentication using MSAL.
Provides login flow, token management, user session handling,
and Azure AD user directory queries.
============================================================================
"""

from auth.microsoft import MicrosoftAuth, require_auth, get_current_user
from auth.graph_users import fetch_domain_users, render_user_select

__all__ = [
    "MicrosoftAuth", "require_auth", "get_current_user",
    "fetch_domain_users", "render_user_select",
]
