"""
============================================================================
AgGrid Table Component
============================================================================
Professional data tables with filtering, sorting, pagination, and export.
Wraps streamlit-aggrid with sensible defaults and easy customization.

Usage:
    from components import render_aggrid_table, AgGridConfig

    response = render_aggrid_table(
        df,
        config=AgGridConfig(page_size=25, enable_export=True),
    )
    selected_rows = response.selected_rows
============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode


@dataclass
class AgGridConfig:
    """Configuration object for AgGrid tables."""

    # Pagination
    enable_pagination: bool = True
    page_size: int = 20
    page_size_options: list[int] = field(default_factory=lambda: [10, 20, 50, 100])

    # Selection
    selection_mode: Literal["single", "multiple", "disabled"] = "disabled"

    # Features
    enable_sidebar: bool = True          # Column visibility & filter sidebar
    enable_export: bool = True           # CSV export button
    enable_quick_filter: bool = True     # Global search box
    enable_column_filter: bool = True    # Per-column filters
    enable_sorting: bool = True          # Column sorting
    enable_resizing: bool = True         # Column resizing

    # Appearance
    theme: Literal["streamlit", "alpine", "balham", "material"] = "streamlit"
    height: int = 500
    fit_columns: bool = True             # Auto-fit columns to grid width
    wrap_text: bool = False              # Wrap long text in cells

    # Editable
    editable: bool = False

    # Custom column definitions (column_name → dict of AgGrid column props)
    column_config: dict[str, dict[str, Any]] = field(default_factory=dict)


def render_aggrid_table(
    df: pd.DataFrame,
    config: AgGridConfig | None = None,
    key: str | None = None,
) -> Any:
    """
    Render a professional AgGrid table with advanced features.

    Args:
        df: DataFrame to display.
        config: Optional AgGridConfig for customization.
        key: Unique Streamlit widget key.

    Returns:
        AgGrid response object. Access `.data` for the displayed DataFrame
        and `.selected_rows` for any selected rows.
    """
    if config is None:
        config = AgGridConfig()

    if df.empty:
        st.info("No data to display.")
        return None

    # --- Quick filter search box ---
    if config.enable_quick_filter:
        search_term = st.text_input(
            "🔍 Search",
            placeholder="Type to filter across all columns…",
            key=f"aggrid_search_{key or 'default'}",
        )
    else:
        search_term = ""

    # --- Build grid options ---
    gb = GridOptionsBuilder.from_dataframe(df)

    # Default column settings
    gb.configure_default_column(
        filterable=config.enable_column_filter,
        sortable=config.enable_sorting,
        resizable=config.enable_resizing,
        editable=config.editable,
        wrapText=config.wrap_text,
        autoHeight=config.wrap_text,
    )

    # Pagination
    if config.enable_pagination:
        gb.configure_pagination(
            paginationAutoPageSize=False,
            paginationPageSize=config.page_size,
        )

    # Selection
    if config.selection_mode != "disabled":
        gb.configure_selection(
            selection_mode=config.selection_mode,
            use_checkbox=True,
        )

    # Sidebar (column visibility + filters panel)
    if config.enable_sidebar:
        gb.configure_side_bar(filters_panel=True, columns_panel=True)

    # Apply custom column configs
    for col_name, col_props in config.column_config.items():
        if col_name in df.columns:
            gb.configure_column(col_name, **col_props)

    # Auto-size columns
    if config.fit_columns:
        gb.configure_grid_options(domLayout="normal")

    grid_options = gb.build()

    # Apply quick filter
    if search_term:
        grid_options["quickFilterText"] = search_term

    # --- Render ---
    response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        theme=config.theme,
        height=config.height,
        allow_unsafe_jscode=True,
        key=key,
    )

    # --- Export button ---
    if config.enable_export:
        _render_export_button(response.data, key)

    return response


def _render_export_button(df: pd.DataFrame, key: str | None) -> None:
    """Render a CSV download button below the table."""
    if df is not None and not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export CSV",
            data=csv,
            file_name="export.csv",
            mime="text/csv",
            key=f"export_{key or 'default'}",
        )
