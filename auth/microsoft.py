"""
============================================================================
Microsoft 365 Authentication (MSAL)
============================================================================
Handles OAuth2 authorization code flow for Streamlit apps.

This implementation uses a DIRECT token exchange approach instead of
MSAL's initiate_auth_code_flow, because Streamlit's session_state is
lost when the browser redirects to Microsoft and back (cold reload).

Usage:
    from auth import require_auth, get_current_user

    # In your page — redirects to login if not authenticated
    require_auth()
    user = get_current_user()
    st.write(f"Hello, {user['name']}")

Setup:
    1. Register an app in Azure Portal → Azure Active Directory → App registrations
    2. Add a Web redirect URI matching AZURE_REDIRECT_URI in .env
    3. Create a client secret under Certificates & secrets
    4. Copy Client ID, Tenant ID, and Secret into your .env file
============================================================================
"""

from __future__ import annotations

import base64
import urllib.parse
import uuid
from typing import Any

import msal
import requests
import streamlit as st

from config.settings import get_settings


class MicrosoftAuth:
    """
    Encapsulates MSAL confidential client operations.
    Uses acquire_token_by_authorization_code (direct exchange) which
    does NOT require storing the auth flow in session_state.
    """

    GRAPH_ME_ENDPOINT = "https://graph.microsoft.com/v1.0/me"
    GRAPH_PHOTO_ENDPOINT = "https://graph.microsoft.com/v1.0/me/photo/$value"

    def __init__(self) -> None:
        self._settings = get_settings()
        self._app: msal.ConfidentialClientApplication | None = None

    # ------------------------------------------------------------------
    # MSAL Client
    # ------------------------------------------------------------------

    @property
    def msal_app(self) -> msal.ConfidentialClientApplication:
        """Lazy-initialized MSAL confidential client."""
        if self._app is None:
            self._app = msal.ConfidentialClientApplication(
                client_id=self._settings.azure_client_id,
                client_credential=self._settings.azure_client_secret,
                authority=self._settings.azure_authority,
            )
        return self._app

    # ------------------------------------------------------------------
    # Auth Flow — Direct Authorization Code Exchange
    # ------------------------------------------------------------------

    def get_auth_url(self) -> str:
        """
        Build the Microsoft login URL manually.
        This avoids initiate_auth_code_flow and the need to persist
        the flow object across redirects.
        """
        params = {
            "client_id": self._settings.azure_client_id,
            "response_type": "code",
            "redirect_uri": self._settings.azure_redirect_uri,
            "response_mode": "query",
            "scope": " ".join(self._settings.azure_scopes),
            "state": str(uuid.uuid4()),
        }
        auth_endpoint = f"{self._settings.azure_authority}/oauth2/v2.0/authorize"
        return f"{auth_endpoint}?{urllib.parse.urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> dict[str, Any] | None:
        """
        Exchange an authorization code for an access token.
        Uses MSAL's acquire_token_by_authorization_code which works
        without needing the original auth flow object.

        Args:
            code: The authorization code from the query string.

        Returns:
            Token result dict with 'access_token', or None on failure.
        """
        result = self.msal_app.acquire_token_by_authorization_code(
            code=code,
            scopes=self._settings.azure_scopes,
            redirect_uri=self._settings.azure_redirect_uri,
        )

        if "access_token" in result:
            st.session_state["token"] = result
            # Fetch and cache user profile
            user = self._fetch_user_profile(result["access_token"])
            st.session_state["user"] = user
            return result

        # Log error details for debugging
        error = result.get("error_description") or result.get("error", "Unknown error")
        st.session_state["_auth_error"] = error
        return None

    def logout(self) -> None:
        """Clear all authentication state from the session."""
        for key in ("token", "user", "_auth_error"):
            st.session_state.pop(key, None)

    # ------------------------------------------------------------------
    # User Profile
    # ------------------------------------------------------------------

    def _fetch_user_profile(self, access_token: str) -> dict[str, Any]:
        """Fetch the signed-in user's profile and photo from Microsoft Graph."""
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get(self.GRAPH_ME_ENDPOINT, headers=headers, timeout=10)
        if resp.ok:
            data = resp.json()
            profile = {
                "name": data.get("displayName", "User"),
                "email": data.get("mail") or data.get("userPrincipalName", ""),
                "job_title": data.get("jobTitle", ""),
                "id": data.get("id", ""),
                "photo": None,
            }
            # Fetch profile photo (binary JPEG/PNG)
            profile["photo"] = self._fetch_user_photo(access_token)
            return profile
        return {"name": "User", "email": "", "job_title": "", "id": "", "photo": None}

    def _fetch_user_photo(self, access_token: str) -> str | None:
        """Fetch the user's profile photo as a base64 data URI.

        Returns:
            A data URI string like 'data:image/jpeg;base64,...' or None if
            the user has no photo set.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            resp = requests.get(self.GRAPH_PHOTO_ENDPOINT, headers=headers, timeout=10)
            if resp.ok and resp.content:
                content_type = resp.headers.get("Content-Type", "image/jpeg")
                b64 = base64.b64encode(resp.content).decode("utf-8")
                return f"data:{content_type};base64,{b64}"
        except Exception:
            pass
        return None


# ======================================================================
# Convenience helpers — use these in your pages
# ======================================================================

_auth_instance: MicrosoftAuth | None = None


def _get_auth() -> MicrosoftAuth:
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = MicrosoftAuth()
    return _auth_instance


def is_authenticated() -> bool:
    """Check if the current session has a valid token."""
    return "user" in st.session_state and st.session_state["user"] is not None


def get_current_user() -> dict[str, Any]:
    """
    Return the current authenticated user dict.
    Keys: name, email, job_title, id
    """
    return st.session_state.get("user", {"name": "Guest", "email": "", "job_title": "", "id": ""})


def require_auth() -> None:
    """
    Gate that blocks page rendering if the user is not authenticated.
    Shows a login button that redirects to Microsoft login.
    When auth is disabled in settings, it auto-creates a dev user.
    """
    settings = get_settings()

    # --- Dev mode bypass ---
    if not settings.enable_auth:
        if "user" not in st.session_state:
            st.session_state["user"] = {
                "name": "Dev User",
                "email": "dev@localhost",
                "job_title": "Developer",
                "id": "dev-000",
            }
        return

    # --- Production auth flow ---
    if is_authenticated():
        return

    # Check if we're returning from a redirect with an authorization code.
    # IMPORTANT: Clear the code from query params FIRST to prevent Streamlit's
    # automatic reruns from trying to redeem the same code twice (AADSTS54005).
    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]
        # Immediately clear query params so reruns don't re-trigger exchange
        st.query_params.clear()

        auth = _get_auth()
        result = auth.exchange_code_for_token(code)
        if result:
            st.rerun()
        else:
            error_detail = st.session_state.pop("_auth_error", "Unknown error")
            st.error(f"Authentication failed: {error_detail}")

    # Show login screen
    _render_login_page()
    st.stop()


def do_logout() -> None:
    """Log out the current user and rerun."""
    auth = _get_auth()
    auth.logout()
    st.rerun()


# ======================================================================
# Login UI
# ======================================================================

def _render_login_page() -> None:
    """Render a professional login page with Microsoft sign-in button."""
    settings = get_settings()

    ms_icon = "https://img.icons8.com/?size=100&id=22989&format=png&color=000000"

    # Encode local logo as base64 data URI for st.html
    import base64 as _b64
    from pathlib import Path as _Path
    _logo_path = _Path(__file__).resolve().parent.parent / "img" / "logo_ibtest.png"
    _logo_uri = ""
    if _logo_path.exists():
        _logo_b64 = _b64.b64encode(_logo_path.read_bytes()).decode("utf-8")
        _logo_uri = f"data:image/png;base64,{_logo_b64}"

    auth_url = _get_auth().get_auth_url() if settings.azure_client_id else "#"
    disabled_style = "pointer-events:none; opacity:0.5;" if not settings.azure_client_id else ""

    html = (
        '<div style="display:flex; flex-direction:column; align-items:center;'
        ' justify-content:center; min-height:65vh; text-align:center;">'
        '  <div style="background:white; border:1px solid #E5E7EB; border-radius:16px;'
        '              padding:2.5rem 2.5rem 2rem; max-width:500px; width:100%;'
        '              box-shadow:0 4px 24px rgba(0,0,0,0.08);">'
        + (f'    <img src="{_logo_uri}" alt="Logo"'
           '         style="width:140px; margin:0 auto 1rem; display:block;" />'
           if _logo_uri else '')
        + '    <h1 style="margin:0 0 0.4rem; color:#1E1E1E; font-weight:800;'
        '               font-size:2.2rem; letter-spacing:-0.5px;">'
        f'      {settings.app_name}'
        '    </h1>'
        '    <p style="color:#6B7280; margin:0 0 2rem; font-size:0.95rem; line-height:1.4;">'
        f'      {settings.app_description}'
        '    </p>'
        f'    <a href="{auth_url}"'
        '       style="display:flex; align-items:center; justify-content:center; gap:0.6rem;'
        '              background:#1E1E1E; color:white; text-decoration:none;'
        '              padding:0.75rem 1.5rem; border-radius:8px; font-size:0.95rem;'
        f'              font-weight:600; {disabled_style}">'
        f'      <img src="{ms_icon}" alt="Microsoft" style="width:40px; height:40px;" />'
        '       Iniciar sesi\u00f3n con Microsoft 365'
        '    </a>'
        '    <div style="display:flex; align-items:center; gap:1rem; margin:1.5rem 0 1rem;">'
        '      <div style="flex:1; height:1px; background:#E5E7EB;"></div>'
        '      <span style="color:#9CA3AF; font-size:0.8rem; white-space:nowrap;">'
        '        Acceso corporativo'
        '      </span>'
        '      <div style="flex:1; height:1px; background:#E5E7EB;"></div>'
        '    </div>'
        '    <p style="color:#9CA3AF; font-size:0.82rem; margin:0; line-height:1.5;">'
        '      Usa tu cuenta corporativa de Microsoft 365 para acceder al sistema.'
        '    </p>'
        '  </div>'
        '</div>'
    )

    st.html(html)

    if not settings.azure_client_id:
        st.warning(
            "⚠️ Azure AD is not configured. "
            "Set `AZURE_CLIENT_ID` in your `.env` file, "
            "or set `ENABLE_AUTH=false` to use dev mode."
        )
