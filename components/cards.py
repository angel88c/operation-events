"""
============================================================================
Card Components
============================================================================
Metric cards, info cards, and KPI rows for dashboard layouts.

Usage:
    from components import render_metric_card, render_metric_row

    render_metric_row([
        {"label": "Revenue", "value": "$1.2M", "delta": "+12%", "delta_color": "normal"},
        {"label": "Users",   "value": "8,421", "delta": "+3.2%"},
        {"label": "Orders",  "value": "1,893", "delta": "-1.1%", "delta_color": "inverse"},
    ])
============================================================================
"""

from __future__ import annotations

from typing import Any, Literal

import streamlit as st

from config.theme import theme


def render_metric_card(
    label: str,
    value: str | int | float,
    delta: str | None = None,
    delta_color: Literal["normal", "inverse", "off"] = "normal",
    icon: str = "",
    help_text: str = "",
) -> None:
    """
    Render a single metric card using st.metric with optional icon prefix.

    Args:
        label: Metric label.
        value: Metric value (displayed prominently).
        delta: Delta string (e.g. "+12%").
        delta_color: How to color the delta.
        icon: Optional emoji/icon prefix for the label.
        help_text: Tooltip help text.
    """
    display_label = f"{icon}  {label}" if icon else label
    st.metric(
        label=display_label,
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text or None,
    )


def render_metric_row(
    metrics: list[dict[str, Any]],
    columns: int | None = None,
) -> None:
    """
    Render a row of metric cards in equal-width columns.

    Args:
        metrics: List of dicts with keys: label, value, delta (optional),
                 delta_color (optional), icon (optional), help_text (optional).
        columns: Number of columns. Defaults to len(metrics).
    """
    n = columns or len(metrics)
    cols = st.columns(n)
    for idx, m in enumerate(metrics):
        with cols[idx % n]:
            render_metric_card(
                label=m.get("label", ""),
                value=m.get("value", 0),
                delta=m.get("delta"),
                delta_color=m.get("delta_color", "normal"),
                icon=m.get("icon", ""),
                help_text=m.get("help_text", ""),
            )


def render_info_card(
    title: str,
    content: str,
    icon: str = "ℹ️",
    color: str | None = None,
) -> None:
    """
    Render an informational card with custom HTML styling.

    Args:
        title: Card title.
        content: Card body text (supports HTML).
        icon: Emoji or icon.
        color: Left border accent color. Defaults to primary.
    """
    accent = color or theme.colors.primary
    st.markdown(
        f"""
        <div style="
            background: {theme.colors.surface};
            border-left: 4px solid {accent};
            border-radius: {theme.border_radius};
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
            box-shadow: {theme.shadow_sm};
        ">
            <div style="font-size:1.1rem; font-weight:600; color:{theme.colors.text_primary};
                        margin-bottom:0.4rem;">
                {icon} {title}
            </div>
            <div style="color:{theme.colors.text_secondary}; font-size:0.9rem; line-height:1.5;">
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
