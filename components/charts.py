"""
============================================================================
Chart Components (Plotly)
============================================================================
Professional, reusable chart wrappers with consistent theming.
All charts follow the application color palette and are fully interactive.

Usage:
    from components import render_bar_chart, render_line_chart

    render_bar_chart(df, x="month", y="revenue", title="Monthly Revenue")
    render_line_chart(df, x="date", y=["sales", "returns"], title="Trends")
============================================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config.theme import theme


# ======================================================================
# Shared layout defaults
# ======================================================================

def _base_layout(**overrides: Any) -> dict[str, Any]:
    """Return a base Plotly layout dict with professional styling."""
    layout = dict(
        font=dict(family="Segoe UI, sans-serif", color=theme.colors.text_primary),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
        xaxis=dict(
            showgrid=False,
            linecolor=theme.colors.border,
            linewidth=1,
        ),
        yaxis=dict(
            gridcolor="#F0F0F0",
            gridwidth=1,
            linecolor=theme.colors.border,
            linewidth=1,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Segoe UI, sans-serif",
        ),
    )
    layout.update(overrides)
    return layout


# ======================================================================
# Generic renderer
# ======================================================================

def render_plotly_chart(
    fig: go.Figure,
    use_container_width: bool = True,
    key: str | None = None,
) -> None:
    """
    Render any Plotly figure with consistent styling applied.
    Use this when you build a custom figure and want theme consistency.
    """
    fig.update_layout(**_base_layout())
    st.plotly_chart(fig, width="stretch" if use_container_width else "content", key=key)


# ======================================================================
# Bar Chart
# ======================================================================

def render_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str = "",
    color: str | None = None,
    orientation: str = "v",
    barmode: str = "group",
    key: str | None = None,
) -> None:
    """
    Professional bar chart.

    Args:
        df: Source DataFrame.
        x: Column for x-axis.
        y: Column(s) for y-axis. Pass a list for grouped bars.
        title: Chart title.
        color: Column for color grouping.
        orientation: 'v' (vertical) or 'h' (horizontal).
        barmode: 'group', 'stack', 'overlay', 'relative'.
        key: Streamlit widget key.
    """
    fig = px.bar(
        df, x=x, y=y, color=color, title=title,
        orientation=orientation, barmode=barmode,
        color_discrete_sequence=list(theme.chart_colors.categorical),
    )
    fig.update_layout(**_base_layout(title=dict(text=title, font=dict(size=16, color=theme.colors.text_primary))))
    fig.update_traces(marker_line_width=0, opacity=0.9)
    st.plotly_chart(fig, width="stretch", key=key)


# ======================================================================
# Line Chart
# ======================================================================

def render_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str = "",
    color: str | None = None,
    markers: bool = True,
    key: str | None = None,
) -> None:
    """
    Professional line chart with optional markers.

    Args:
        df: Source DataFrame.
        x: Column for x-axis (typically a date or sequential value).
        y: Column(s) for y-axis.
        title: Chart title.
        color: Column for color grouping.
        markers: Show data point markers.
        key: Streamlit widget key.
    """
    fig = px.line(
        df, x=x, y=y, color=color, title=title, markers=markers,
        color_discrete_sequence=list(theme.chart_colors.categorical),
    )
    fig.update_layout(**_base_layout(title=dict(text=title, font=dict(size=16))))
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, width="stretch", key=key)


# ======================================================================
# Pie / Donut Chart
# ======================================================================

def render_pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str = "",
    hole: float = 0.4,
    key: str | None = None,
) -> None:
    """
    Professional donut/pie chart.

    Args:
        df: Source DataFrame.
        names: Column for slice labels.
        values: Column for slice values.
        title: Chart title.
        hole: 0 for pie, 0.3–0.5 for donut.
        key: Streamlit widget key.
    """
    fig = px.pie(
        df, names=names, values=values, title=title, hole=hole,
        color_discrete_sequence=list(theme.chart_colors.categorical),
    )
    fig.update_layout(**_base_layout(title=dict(text=title, font=dict(size=16))))
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, width="stretch", key=key)


# ======================================================================
# Area Chart
# ======================================================================

def render_area_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str = "",
    color: str | None = None,
    key: str | None = None,
) -> None:
    """Professional stacked area chart."""
    fig = px.area(
        df, x=x, y=y, color=color, title=title,
        color_discrete_sequence=list(theme.chart_colors.categorical),
    )
    fig.update_layout(**_base_layout(title=dict(text=title, font=dict(size=16))))
    st.plotly_chart(fig, width="stretch", key=key)


# ======================================================================
# KPI Indicator Chart
# ======================================================================

def render_kpi_chart(
    value: float,
    reference: float | None = None,
    title: str = "",
    prefix: str = "",
    suffix: str = "",
    key: str | None = None,
) -> None:
    """
    Render a KPI indicator gauge.

    Args:
        value: Current value.
        reference: Previous/target value for delta calculation.
        title: KPI title.
        prefix: Value prefix (e.g. '$').
        suffix: Value suffix (e.g. '%').
        key: Streamlit widget key.
    """
    fig = go.Figure(
        go.Indicator(
            mode="number+delta" if reference is not None else "number",
            value=value,
            delta=dict(reference=reference, relative=True, valueformat=".1%") if reference else None,
            title=dict(text=title, font=dict(size=14, color=theme.colors.text_secondary)),
            number=dict(
                prefix=prefix,
                suffix=suffix,
                font=dict(size=36, color=theme.colors.text_primary, family="Segoe UI"),
            ),
        )
    )
    fig.update_layout(
        height=150,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch", key=key)
