"""
============================================================================
Pantalla de Reportes y Análisis (RF-003)
============================================================================
Dashboard con gráficos Pareto, tendencias mensuales e insights.
Se implementará en el Milestone 4.

Referencia: specs/operation-events.md — RF-003, Milestone 4
============================================================================
"""

from __future__ import annotations

import streamlit as st

from components.navigation import render_page_header
from config.theme import theme


def render() -> None:
    """Render the reports and analysis page (placeholder)."""
    render_page_header(
        title="Reportes y Análisis",
        description="Análisis gráfico de eventos operativos",
        icon="📊",
    )

    st.markdown(
        f"""
        <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                    border-radius:{theme.border_radius}; padding:3rem; text-align:center;
                    margin-top:2rem;">
            <h2 style="color:{theme.colors.text_secondary}; margin-bottom:0.5rem;">
                🚧 Próximamente — Milestone 4
            </h2>
            <p style="color:{theme.colors.text_muted}; font-size:0.95rem;">
                Esta pantalla mostrará gráficos Pareto de causas, tendencia mensual de eventos,
                insights importantes y opciones de exportación de reportes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
