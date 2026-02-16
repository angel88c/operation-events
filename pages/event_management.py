"""
============================================================================
Pantalla de Gestión de Eventos (RF-002)
============================================================================
Tabla editable para dar seguimiento a eventos con acciones correctivas
y preventivas. Se implementará en el Milestone 3.

Referencia: specs/operation-events.md — RF-002, Milestone 3
============================================================================
"""

from __future__ import annotations

import streamlit as st

from components.navigation import render_page_header
from config.theme import theme


def render() -> None:
    """Render the event management page (placeholder)."""
    render_page_header(
        title="Gestión de Eventos",
        description="Seguimiento y gestión de eventos operativos",
        icon="📋",
    )

    st.markdown(
        f"""
        <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                    border-radius:{theme.border_radius}; padding:3rem; text-align:center;
                    margin-top:2rem;">
            <h2 style="color:{theme.colors.text_secondary}; margin-bottom:0.5rem;">
                🚧 Próximamente — Milestone 3
            </h2>
            <p style="color:{theme.colors.text_muted}; font-size:0.95rem;">
                Esta pantalla permitirá ver todos los eventos en una tabla editable,
                asignar acciones correctivas/preventivas, cambiar status y re-asignar responsables.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
