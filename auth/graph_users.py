"""
============================================================================
Microsoft Graph — User Directory
============================================================================
Functions to query users from your Azure AD tenant via Microsoft Graph API.
Useful for user pickers, assignment dropdowns, and directory lookups.

Requirements:
    - The Azure AD app registration needs the **User.Read.All** permission
      (delegated or application). Admin consent is required for this scope.
    - If using delegated permissions, add "User.Read.All" to azure_scopes
      in config/settings.py.
    - If using application permissions (client credentials), grant admin
      consent in Azure Portal and use acquire_token_for_client().

Usage:
    from auth.graph_users import fetch_domain_users, render_user_select

    # Fetch users programmatically
    users = fetch_domain_users(domain="ibtest.com")

    # Render a selectbox and get the selected user dict
    selected = render_user_select(domain="ibtest.com", label="Assign to")
    if selected:
        st.write(selected["displayName"], selected["mail"])
============================================================================
"""

from __future__ import annotations

from typing import Any

import requests
import streamlit as st

from config.settings import get_settings


GRAPH_USERS_ENDPOINT = "https://graph.microsoft.com/v1.0/users"


# ======================================================================
# Data Fetching
# ======================================================================

def _get_access_token() -> str | None:
    """
    Retrieve the current user's access token from session_state.
    Returns None if not authenticated.
    """
    token = st.session_state.get("token")
    if token and "access_token" in token:
        return token["access_token"]
    return None


def _get_client_token() -> str | None:
    """
    Acquire an application-level token using client credentials.
    This does NOT require a logged-in user but needs User.Read.All
    application permission with admin consent.
    """
    import msal
    settings = get_settings()
    if not settings.azure_client_id or not settings.azure_client_secret:
        return None

    app = msal.ConfidentialClientApplication(
        client_id=settings.azure_client_id,
        client_credential=settings.azure_client_secret,
        authority=settings.azure_authority,
    )
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"],
    )
    if "access_token" in result:
        return result["access_token"]
    return None


def fetch_domain_users(
    domain: str = "",
    use_client_credentials: bool = True,
    select_fields: list[str] | None = None,
    max_results: int = 999,
) -> list[dict[str, Any]]:
    """
    Fetch users from Azure AD, optionally filtered by email domain.

    Args:
        domain: Email domain to filter (e.g. "ibtest.com"). If empty,
                returns all users.
        use_client_credentials: If True, uses app-level token (no user
                needed). If False, uses the logged-in user's token.
        select_fields: Graph API $select fields. Defaults to common fields.
        max_results: Maximum number of users to return.

    Returns:
        List of user dicts with keys like displayName, mail, id, jobTitle, etc.
    """
    # Get token
    if use_client_credentials:
        token = _get_client_token()
    else:
        token = _get_access_token()

    if not token:
        st.warning("No access token available. Check authentication and permissions.")
        return []

    # Build query
    if select_fields is None:
        select_fields = [
            "id", "displayName", "mail", "userPrincipalName",
            "jobTitle", "department", "officeLocation",
        ]

    params: dict[str, Any] = {
        "$select": ",".join(select_fields),
        "$top": min(max_results, 999),
        "$orderby": "displayName",
    }

    # Filter by domain — only real user accounts (exclude rooms, resources,
    # distribution lists, shared mailboxes, etc.)
    person_filter = "userType eq 'Member' and accountEnabled eq true"
    if domain:
        domain_filter = (
            f"endsWith(mail, '@{domain}') or "
            f"endsWith(userPrincipalName, '@{domain}')"
        )
        params["$filter"] = f"({domain_filter}) and {person_filter}"
        # endsWith requires $count and ConsistencyLevel header
        params["$count"] = "true"
    else:
        params["$filter"] = person_filter

    headers: dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "ConsistencyLevel": "eventual",
    }

    all_users: list[dict[str, Any]] = []

    try:
        url: str | None = GRAPH_USERS_ENDPOINT
        while url and len(all_users) < max_results:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            if not resp.ok:
                error_msg = resp.json().get("error", {}).get("message", resp.text)
                st.error(f"Graph API error: {error_msg}")
                return all_users

            data = resp.json()
            users = data.get("value", [])
            all_users.extend(users)

            # Pagination
            url = data.get("@odata.nextLink")
            params = {}  # nextLink already contains params

    except Exception as e:
        st.error(f"Error fetching users: {e}")

    return all_users[:max_results]


@st.cache_data(ttl=300, show_spinner="Loading users…")
def _cached_fetch_domain_users(
    domain: str,
    use_client_credentials: bool,
    max_results: int,
) -> list[dict[str, Any]]:
    """Cached wrapper — results are cached for 5 minutes."""
    return fetch_domain_users(
        domain=domain,
        use_client_credentials=use_client_credentials,
        max_results=max_results,
    )


# ======================================================================
# UI Component
# ======================================================================

def render_user_select(
    domain: str = "",
    label: str = "Select User",
    use_client_credentials: bool = True,
    include_email: bool = True,
    max_results: int = 999,
    key: str = "user_select",
    cache: bool = True,
) -> dict[str, Any] | None:
    """
    Render a selectbox populated with Azure AD users.

    Args:
        domain: Email domain filter (e.g. "ibtest.com").
        label: Selectbox label.
        use_client_credentials: Use app-level token (True) or user token (False).
        include_email: Show email next to name in the dropdown.
        max_results: Max users to load.
        key: Streamlit widget key.
        cache: Cache results for 5 minutes.

    Returns:
        The selected user dict, or None if no selection.
    """
    # Fetch users
    if cache:
        users = _cached_fetch_domain_users(domain, use_client_credentials, max_results)
    else:
        users = fetch_domain_users(domain, use_client_credentials, max_results)

    if not users:
        st.info("No users found.")
        return None

    # Build display options
    def _display_name(u: dict[str, Any]) -> str:
        name = u.get("displayName", "Unknown")
        email = u.get("mail") or u.get("userPrincipalName", "")
        if include_email and email:
            return f"{name} ({email})"
        return name

    options = [""] + [_display_name(u) for u in users]

    selected_label = st.selectbox(label, options=options, key=key)

    if not selected_label:
        return None

    # Find the matching user
    idx = options.index(selected_label) - 1  # offset by 1 for the empty option
    if 0 <= idx < len(users):
        return users[idx]

    return None
