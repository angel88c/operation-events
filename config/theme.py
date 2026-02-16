"""
============================================================================
Theme & Styling Constants
============================================================================
Centralized theme configuration for consistent UI across the application.
Use these constants in all pages and components for visual consistency.
============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ColorPalette:
    """Application color palette aligned with Microsoft Fluent Design."""

    primary: str = "#0078D4"
    primary_dark: str = "#005A9E"
    primary_light: str = "#DEECF9"
    secondary: str = "#6B7280"
    success: str = "#107C10"
    warning: str = "#FFB900"
    danger: str = "#D13438"
    info: str = "#0078D4"
    background: str = "#FFFFFF"
    surface: str = "#F9FAFB"
    border: str = "#E5E7EB"
    text_primary: str = "#1E1E1E"
    text_secondary: str = "#6B7280"
    text_muted: str = "#9CA3AF"


@dataclass(frozen=True)
class ChartColors:
    """Color sequences for charts and visualizations."""

    sequential: tuple[str, ...] = (
        "#0078D4", "#2B88D8", "#71AFE5", "#C7E0F4", "#DEECF9",
    )
    categorical: tuple[str, ...] = (
        "#0078D4", "#107C10", "#FFB900", "#D13438", "#5C2D91",
        "#008272", "#E3008C", "#4F6BED", "#CA5010", "#0B6A0B",
    )
    diverging: tuple[str, ...] = (
        "#D13438", "#E87D7F", "#F4C7C3", "#F0F2F6",
        "#C7E0F4", "#71AFE5", "#0078D4",
    )


@dataclass(frozen=True)
class Spacing:
    """Spacing constants for consistent layout."""

    xs: str = "0.25rem"
    sm: str = "0.5rem"
    md: str = "1rem"
    lg: str = "1.5rem"
    xl: str = "2rem"
    xxl: str = "3rem"


@dataclass(frozen=True)
class Theme:
    """Master theme object combining all design tokens."""

    colors: ColorPalette = field(default_factory=ColorPalette)
    chart_colors: ChartColors = field(default_factory=ChartColors)
    spacing: Spacing = field(default_factory=Spacing)
    border_radius: str = "8px"
    shadow_sm: str = "0 1px 2px rgba(0,0,0,0.05)"
    shadow_md: str = "0 4px 6px rgba(0,0,0,0.07)"
    shadow_lg: str = "0 10px 15px rgba(0,0,0,0.1)"


# Singleton theme instance — import this in your pages/components
theme = Theme()


def get_custom_css() -> str:
    """
    Returns custom CSS to inject into the Streamlit app for enhanced styling.
    Call this once in your main app entry point via st.markdown(unsafe_allow_html=True).
    """
    return f"""
    <style>
        /* --- Global Overrides --- */
        .stApp {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* --- Metric Cards --- */
        div[data-testid="stMetric"] {{
            background-color: {theme.colors.surface};
            border: 1px solid {theme.colors.border};
            border-radius: {theme.border_radius};
            padding: 1rem 1.25rem;
            box-shadow: {theme.shadow_sm};
        }}
        div[data-testid="stMetric"] label {{
            color: {theme.colors.text_secondary};
            font-size: 0.85rem;
            font-weight: 500;
        }}
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
            color: {theme.colors.text_primary};
            font-weight: 700;
        }}

        /* --- Sidebar --- */
        section[data-testid="stSidebar"] {{
            background-color: #FAFBFC;
            border-right: 1px solid {theme.colors.border};
        }}
        section[data-testid="stSidebar"] .stRadio > label {{
            font-weight: 600;
            color: {theme.colors.text_primary};
        }}

        /* --- Buttons --- */
        .stButton > button {{
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.15s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: {theme.shadow_md};
        }}

        /* --- Tabs --- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 6px 6px 0 0;
            font-weight: 600;
        }}

        /* --- DataFrames & Tables --- */
        .stDataFrame {{
            border-radius: {theme.border_radius};
            overflow: hidden;
        }}

        /* --- Cards helper class --- */
        .card {{
            background: {theme.colors.background};
            border: 1px solid {theme.colors.border};
            border-radius: {theme.border_radius};
            padding: 1.5rem;
            box-shadow: {theme.shadow_sm};
            margin-bottom: 1rem;
        }}

        /* --- Status badges --- */
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge-success {{ background: #E6F4EA; color: {theme.colors.success}; }}
        .badge-warning {{ background: #FFF8E1; color: #B8860B; }}
        .badge-danger  {{ background: #FDECEA; color: {theme.colors.danger}; }}
        .badge-info    {{ background: {theme.colors.primary_light}; color: {theme.colors.primary}; }}

        /* --- Hide Streamlit branding (optional) --- */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
    </style>
    """
