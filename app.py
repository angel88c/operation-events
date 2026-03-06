"""
============================================================================
Operation Events — Main Entry Point
============================================================================
Captura y análisis de eventos operativos en producción.

Run with:
    streamlit run app.py

For development without Microsoft 365 auth:
    Set ENABLE_AUTH=false in your .env file
============================================================================
"""

from __future__ import annotations

import streamlit as st

# --- Page config (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="Operation Events",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Imports (after set_page_config) ---
from auth.microsoft import require_auth
from components.navigation import render_sidebar
from config.theme import get_custom_css
from pages import capture, event_management, reports, settings_page


def main() -> None:
    """Application entry point."""

    # --- Inject custom CSS ---
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # --- Authentication gate ---
    require_auth()

    # --- Sidebar navigation ---
    selected_page = render_sidebar()

    # --- Page router ---
    PAGE_MAP = {
        "Captura":        capture.render,
        "Gestión":        event_management.render,
        "Reportes":       reports.render,
        "Configuración":  settings_page.render,
    }

    page_fn = PAGE_MAP.get(selected_page)
    if page_fn:
        page_fn()
    else:
        st.error(f"Page '{selected_page}' not found.")


if __name__ == "__main__":
    main()
