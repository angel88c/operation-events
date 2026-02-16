"""
============================================================================
Pantalla de Gestión de Eventos (RF-002)
============================================================================
Tabla editable para dar seguimiento a eventos con acciones correctivas
y preventivas.

Features:
    - Tabla AgGrid con datos de Microsoft List
    - Campos editables: Acción Correctiva/Preventiva, Fecha Plan,
      Fecha Real de Cierre, Status
    - Filtro por Responsable con resumen
    - Botón Guardar que persiste cambios en SharePoint

Referencia: specs/operation-events.md — RF-002, Milestone 3
============================================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

from components.navigation import render_page_header
from config.settings import get_settings
from config.theme import theme
from utils.sharepoint import get_all_events, update_event


# ======================================================================
# Constants
# ======================================================================

STATUS_OPTIONS = ["Open", "In Progress", "Closed"]

# Column display configuration: (python_key, display_label, editable, width)
COLUMN_CONFIG = [
    ("id",                "ID",                   False, 70),
    ("persona_detecta",   "Detectó",              False, 140),
    ("tipo_impacto",      "Impacto",              False, 130),
    ("causa",             "Causa",                 False, 150),
    ("numero_proyecto",   "Proyecto",              False, 110),
    ("numero_parte",      "Parte/Plano",           False, 120),
    ("responsable",       "Responsable",           False, 140),
    ("comentarios",       "Comentarios",           False, 160),
    ("fecha_hallazgo",    "Fecha Hallazgo",        False, 120),
    ("accion_correctiva", "Acción Correctiva",     True,  200),
    ("accion_preventiva", "Acción Preventiva",     True,  200),
    ("fecha_plan",        "Fecha Plan",            True,  120),
    ("fecha_real_cierre", "Fecha Real Cierre",     True,  130),
    ("status",            "Status",                True,  110),
]


# ======================================================================
# Data Loading
# ======================================================================

def _load_events() -> pd.DataFrame:
    """Fetch events from SharePoint and return as DataFrame."""
    events = get_all_events()
    if not events:
        return pd.DataFrame()

    df = pd.DataFrame(events)

    # Ensure all expected columns exist
    for key, _, _, _ in COLUMN_CONFIG:
        if key not in df.columns:
            df[key] = ""

    # Order columns
    col_order = [c[0] for c in COLUMN_CONFIG]
    existing = [c for c in col_order if c in df.columns]
    df = df[existing]

    return df


# ======================================================================
# AgGrid Configuration
# ======================================================================

def _build_grid_options(df: pd.DataFrame) -> dict:
    """Build AgGrid options with editable columns."""
    gb = GridOptionsBuilder.from_dataframe(df)

    # Default column settings: no wrap, single line
    gb.configure_default_column(
        resizable=True,
        filterable=True,
        sortable=True,
        editable=False,
        wrapText=False,
        autoHeight=False,
    )

    # Configure each column
    for key, label, editable, width in COLUMN_CONFIG:
        if key not in df.columns:
            continue

        col_opts: dict[str, Any] = {
            "headerName": label,
            "width": width,
            "editable": editable,
        }

        # Status column: dropdown editor
        if key == "status":
            col_opts["cellEditor"] = "agSelectCellEditor"
            col_opts["cellEditorParams"] = {"values": STATUS_OPTIONS}

        # Date columns: format nicely
        if key in ("fecha_hallazgo", "fecha_plan", "fecha_real_cierre"):
            col_opts["type"] = ["dateColumnFilter"]

        # Comentarios: multiline wrap
        if key == "comentarios":
            col_opts["wrapText"] = True
            col_opts["autoHeight"] = True

        # Highlight editable columns
        if editable:
            style = col_opts.get("cellStyle", {})
            style["backgroundColor"] = "#f0f7ff"
            style["borderLeft"] = "2px solid #0078D4"
            col_opts["cellStyle"] = style

        gb.configure_column(key, **col_opts)

    # Selection
    gb.configure_selection(
        selection_mode="single",
        use_checkbox=False,
    )

    # Pagination & grid options
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    gb.configure_grid_options(
        domLayout="normal",
        enableRangeSelection=False,
        stopEditingWhenCellsLoseFocus=True,
    )

    return gb.build()


# ======================================================================
# Save Changes
# ======================================================================

def _save_changes(original_df: pd.DataFrame, edited_df: pd.DataFrame) -> int:
    """
    Compare original and edited DataFrames, save changes to SharePoint.

    Returns:
        Number of rows successfully updated.
    """
    editable_keys = [key for key, _, editable, _ in COLUMN_CONFIG if editable]
    updated_count = 0

    # Build lookup of original rows by item ID
    orig_by_id: dict[str, dict[str, Any]] = {}
    for _, row in original_df.iterrows():
        rid = str(row.get("id", ""))
        if rid:
            orig_by_id[rid] = row.to_dict()

    for _, edited_row in edited_df.iterrows():
        row_id = str(edited_row.get("id", ""))
        if not row_id or row_id not in orig_by_id:
            continue

        orig_row = orig_by_id[row_id]
        changes: dict[str, Any] = {}

        for key in editable_keys:
            if key not in edited_df.columns:
                continue
            new_val = edited_row.get(key)
            old_val = orig_row.get(key)

            # Normalize NaN/None
            if pd.isna(new_val) if not isinstance(new_val, str) else False:
                new_val = ""
            if pd.isna(old_val) if not isinstance(old_val, str) else False:
                old_val = ""

            new_str = str(new_val).strip() if new_val is not None else ""
            old_str = str(old_val).strip() if old_val is not None else ""

            if new_str != old_str:
                changes[key] = new_str if new_str else None

        if changes:
            success = update_event(row_id, changes)
            if success:
                updated_count += 1

    return updated_count


# ======================================================================
# Render Page
# ======================================================================

def render() -> None:
    """Render the event management page."""
    render_page_header(
        title="Gestión de Eventos",
        description="Seguimiento y gestión de eventos operativos",
        icon="📋",
    )

    # --- Toolbar ---
    col_refresh, col_save, col_spacer = st.columns([1, 1, 4])

    with col_refresh:
        refresh = st.button("🔄 Actualizar Datos", key="refresh_events", type="secondary")

    with col_save:
        save = st.button("💾 Guardar Cambios", key="save_events", type="primary")

    # --- Load Data ---
    if refresh or "events_df" not in st.session_state:
        with st.spinner("Cargando eventos desde SharePoint..."):
            df = _load_events()
            st.session_state["events_df"] = df
            st.session_state["events_df_original"] = df.copy()

    df = st.session_state.get("events_df", pd.DataFrame())

    if df.empty:
        st.info("📭 No hay eventos registrados. Captura un evento primero.")
        return

    # --- Filters ---
    st.markdown("---")
    col_filter1, col_filter2, col_filter3 = st.columns(3)

    with col_filter1:
        responsables = ["Todos"] + sorted(df["responsable"].dropna().unique().tolist())
        selected_resp = st.selectbox(
            "Filtrar por Responsable",
            options=responsables,
            key="filter_responsable",
        )

    with col_filter2:
        statuses = ["Todos"] + STATUS_OPTIONS
        selected_status = st.selectbox(
            "Filtrar por Status",
            options=statuses,
            key="filter_status",
        )

    with col_filter3:
        impactos = ["Todos"] + sorted(df["tipo_impacto"].dropna().unique().tolist())
        selected_impacto = st.selectbox(
            "Filtrar por Impacto",
            options=impactos,
            key="filter_impacto",
        )

    # Apply filters
    filtered_df = df.copy()
    if selected_resp != "Todos":
        filtered_df = filtered_df[filtered_df["responsable"] == selected_resp]
    if selected_status != "Todos":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]
    if selected_impacto != "Todos":
        filtered_df = filtered_df[filtered_df["tipo_impacto"] == selected_impacto]

    filtered_df = filtered_df.reset_index(drop=True)

    # --- Summary Metrics ---
    total = len(filtered_df)
    open_count = len(filtered_df[filtered_df["status"] == "Open"]) if "status" in filtered_df.columns else 0
    in_progress = len(filtered_df[filtered_df["status"] == "In Progress"]) if "status" in filtered_df.columns else 0
    closed = len(filtered_df[filtered_df["status"] == "Closed"]) if "status" in filtered_df.columns else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Eventos", total)
    m2.metric("🔴 Open", open_count)
    m3.metric("🟡 In Progress", in_progress)
    m4.metric("🟢 Closed", closed)

    st.markdown("---")

    # --- AgGrid Table ---
    st.markdown(
        f"""<p style="color:{theme.colors.text_muted}; font-size:0.85rem; margin-bottom:0.5rem;">
            💡 Haz doble clic en las celdas con fondo azul para editarlas.
            Después presiona <strong>💾 Guardar Cambios</strong>.
        </p>""",
        unsafe_allow_html=True,
    )

    grid_options = _build_grid_options(filtered_df)

    grid_response = AgGrid(
        filtered_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        data_return_mode=DataReturnMode.AS_INPUT,
        fit_columns_on_grid_load=False,
        height=min(400 + len(filtered_df) * 10, 700),
        theme="streamlit",
        allow_unsafe_jscode=False,
    )

    # --- Save Logic ---
    if save:
        edited_data = grid_response["data"]
        if isinstance(edited_data, pd.DataFrame) and not edited_data.empty:
            original = st.session_state.get("events_df_original", pd.DataFrame())
            with st.spinner("Guardando cambios en SharePoint..."):
                count = _save_changes(original, edited_data)
            if count > 0:
                st.success(f"✅ {count} evento(s) actualizado(s) exitosamente.")
                # Refresh data
                st.session_state.pop("events_df", None)
                st.session_state.pop("events_df_original", None)
                st.rerun()
            else:
                st.info("ℹ️ No se detectaron cambios para guardar.")
        else:
            st.info("ℹ️ No hay datos para guardar.")
