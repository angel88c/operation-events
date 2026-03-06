"""
============================================================================
Reusable UI Components
============================================================================
Import components from here for clean, consistent usage across pages.

    from components import render_aggrid_table, render_plotly_chart, render_metric_card
============================================================================
"""

from components.tables import render_aggrid_table, AgGridConfig
from components.charts import (
    render_plotly_chart,
    render_bar_chart,
    render_line_chart,
    render_pie_chart,
    render_area_chart,
    render_kpi_chart,
)
from components.forms import validated_form, FormField, validate_fields
from components.cards import render_metric_card, render_metric_row, render_info_card
from components.navigation import render_sidebar, render_page_header, render_user_menu

__all__ = [
    "render_aggrid_table", "AgGridConfig",
    "render_plotly_chart", "render_bar_chart", "render_line_chart",
    "render_pie_chart", "render_area_chart", "render_kpi_chart",
    "validated_form", "FormField", "validate_fields",
    "render_metric_card", "render_metric_row", "render_info_card",
    "render_sidebar", "render_page_header", "render_user_menu",
]
