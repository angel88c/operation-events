"""
============================================================================
Navigation & Layout Components
============================================================================
Sidebar navigation, page headers, and user menu.
Uses streamlit-option-menu for a polished sidebar experience.

Usage:
    from components.navigation import render_sidebar, render_page_header

    page = render_sidebar()   # returns selected page name
    render_page_header("Dashboard", "Overview of key metrics")
============================================================================
"""

from __future__ import annotations

from typing import Any

import streamlit as st
from streamlit_option_menu import option_menu

from auth.microsoft import is_authenticated, get_current_user, do_logout
from config.settings import get_settings
from config.theme import theme


# ======================================================================
# Page Registry
# ======================================================================
# Define all navigable pages here. Each entry maps to a page module.
# Icons use Bootstrap Icons names: https://icons.getbootstrap.com/

PAGE_REGISTRY: list[dict[str, str]] = [
    {"name": "Captura",          "icon": "plus-circle"},
    {"name": "Gestión",          "icon": "table"},
    {"name": "Reportes",         "icon": "bar-chart-line"},
    {"name": "Configuración",    "icon": "gear"},
]


# ======================================================================
# Sidebar
# ======================================================================

def render_sidebar() -> str:
    """
    Render the sidebar with navigation menu and user info.

    Returns:
        The name of the currently selected page.
    """
    settings = get_settings()

    with st.sidebar:
        # --- App branding (logo + name) ---
        logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
        with logo_col2:
            st.image("img/logo_ibtest.png", width=120)
        st.markdown(
            f"""
            <div style="text-align:center; padding:0 0 0.5rem;">
                <h3 style="margin:0; color:{theme.colors.primary}; font-weight:700;">
                    {settings.app_name}
                </h3>
                <span style="font-size:0.75rem; color:{theme.colors.text_muted};">
                    v{settings.app_version}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # --- Navigation menu ---
        selected = option_menu(
            menu_title=None,
            options=[p["name"] for p in PAGE_REGISTRY],
            icons=[p["icon"] for p in PAGE_REGISTRY],
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": theme.colors.primary, "font-size": "1rem"},
                "nav-link": {
                    "font-size": "0.9rem",
                    "text-align": "left",
                    "margin": "2px 0",
                    "padding": "0.6rem 1rem",
                    "border-radius": "6px",
                    "--hover-color": theme.colors.primary_light,
                },
                "nav-link-selected": {
                    "background-color": theme.colors.primary,
                    "color": "white",
                    "font-weight": "600",
                },
            },
        )

        # --- Spacer ---
        st.markdown("<div style='flex:1;'></div>", unsafe_allow_html=True)

        # --- User menu ---
        st.markdown("---")
        render_user_menu()

    return selected


# ======================================================================
# User Menu
# ======================================================================

def render_user_menu() -> None:
    """Render user info and logout button in the sidebar."""
    user = get_current_user()

    photo = user.get("photo")

    # Use columns to place avatar next to user info
    col_avatar, col_info = st.columns([1, 3], gap="small")

    with col_avatar:
        if photo:
            # Decode base64 data URI to bytes for st.image (sidebar-safe)
            import base64 as _b64
            try:
                b64_data = photo.split(",", 1)[1]
                img_bytes = _b64.b64decode(b64_data)
                st.image(img_bytes, width=36)
            except Exception:
                st.markdown(f"**{_get_initials(user.get('name', 'U'))}**")
        else:
            st.markdown(
                f"""
                <div style="
                    width:36px; height:36px; border-radius:50%;
                    background:{theme.colors.primary}; color:white;
                    display:flex; align-items:center; justify-content:center;
                    font-weight:700; font-size:0.85rem;
                ">
                    {_get_initials(user.get('name', 'U'))}
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(
            f"""
            <div style="padding-top:2px;">
                <div style="font-weight:600; font-size:0.85rem; color:{theme.colors.text_primary};
                            white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    {user.get('name', 'User')}
                </div>
                <div style="font-size:0.75rem; color:{theme.colors.text_muted};
                            white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    {user.get('email', '')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if is_authenticated() or not get_settings().enable_auth:
        if st.button("🚪 Sign Out", width="stretch", key="btn_logout"):
            do_logout()


# ======================================================================
# Page Header
# ======================================================================

def render_page_header(
    title: str,
    description: str = "",
    icon: str = "",
) -> None:
    """
    Render a consistent page header with title and optional description.

    Args:
        title: Page title.
        description: Subtitle / description text.
        icon: Optional emoji icon.
    """
    header = f"{icon}  {title}" if icon else title
    st.markdown(
        f"""
        <div style="margin-bottom:1.5rem;">
            <h1 style="margin:0 0 0.25rem; font-size:1.75rem; font-weight:700;
                       color:{theme.colors.text_primary};">
                {header}
            </h1>
            {'<p style="margin:0; color:' + theme.colors.text_secondary + '; font-size:0.95rem;">'
             + description + '</p>' if description else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================================
# Helpers
# ======================================================================

def _get_initials(name: str) -> str:
    """Extract up to 2 initials from a display name."""
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[0].upper() if name else "U"
