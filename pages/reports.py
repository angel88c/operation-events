"""
============================================================================
Pantalla de Reportes y Análisis (RF-003)
============================================================================
Dashboard con gráficos Pareto, tendencias mensuales e insights.

Features:
    - Gráfico Pareto de Causas (barras + línea % acumulado)
    - Gráfico de Tendencia Mensual de eventos
    - Insights: Top 3 causas, proyectos con más eventos, recomendaciones
    - Exportar Reporte a Excel
    - Actualizar Datos desde SharePoint

Referencia: specs/operation-events.md — RF-003, Milestone 4
============================================================================
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.navigation import render_page_header
from config.theme import theme
from utils.sharepoint import get_all_events


# ======================================================================
# Data Loading
# ======================================================================

def _load_report_data() -> pd.DataFrame:
    """Fetch events from SharePoint and prepare for reporting."""
    events = get_all_events()
    if not events:
        return pd.DataFrame()

    df = pd.DataFrame(events)

    # Parse fecha_hallazgo to datetime
    if "fecha_hallazgo" in df.columns:
        df["fecha_hallazgo"] = pd.to_datetime(df["fecha_hallazgo"], errors="coerce")
        df["mes"] = df["fecha_hallazgo"].dt.tz_localize(None).dt.to_period("M").astype(str)

    # Fill NaN for grouping columns
    for col in ("causa", "tipo_impacto", "numero_proyecto", "responsable", "status"):
        if col in df.columns:
            df[col] = df[col].fillna("Sin dato")

    return df


# ======================================================================
# Pareto Chart
# ======================================================================

def _render_pareto(
    df: pd.DataFrame,
    column: str = "causa",
    title: str = "Pareto de Causas",
    bar_color: str = "#0078D4",
) -> None:
    """Render a generic Pareto chart for any categorical column."""
    if column not in df.columns or df.empty:
        st.info(f"No hay datos para {title}.")
        return

    counts = df[column].value_counts().reset_index()
    counts.columns = ["Categoría", "Cantidad"]
    counts = counts.sort_values("Cantidad", ascending=False).reset_index(drop=True)

    total = counts["Cantidad"].sum()
    counts["Acumulado"] = counts["Cantidad"].cumsum()
    counts["% Acumulado"] = (counts["Acumulado"] / total * 100).round(1)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=counts["Categoría"],
        y=counts["Cantidad"],
        name="Cantidad",
        marker_color=bar_color,
        text=counts["Cantidad"],
        textposition="outside",
    ))

    fig.add_trace(go.Scatter(
        x=counts["Categoría"],
        y=counts["% Acumulado"],
        name="% Acumulado",
        yaxis="y2",
        mode="lines+markers+text",
        line=dict(color="#D13438", width=2),
        marker=dict(size=6),
        text=counts["% Acumulado"].apply(lambda v: f"{v}%"),
        textposition="top center",
        textfont=dict(size=10),
    ))

    fig.update_layout(
        title=title,
        xaxis_title="",
        yaxis=dict(title="Cantidad", showgrid=True),
        yaxis2=dict(
            title="% Acumulado",
            overlaying="y",
            side="right",
            range=[0, 110],
            showgrid=False,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=80),
        height=380,
    )

    st.plotly_chart(fig, width="stretch")


# ======================================================================
# Events by Project Chart
# ======================================================================

def _render_events_by_project(df: pd.DataFrame) -> None:
    """Render horizontal bar chart of events per project."""
    if "numero_proyecto" not in df.columns or df.empty:
        st.info("No hay datos de proyectos.")
        return

    counts = df["numero_proyecto"].value_counts().reset_index()
    counts.columns = ["Proyecto", "Cantidad"]
    counts = counts.sort_values("Cantidad", ascending=True)  # ascending for horizontal

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=counts["Proyecto"],
        x=counts["Cantidad"],
        orientation="h",
        marker_color="#8764B8",
        text=counts["Cantidad"],
        textposition="outside",
    ))

    fig.update_layout(
        title="Eventos por Proyecto",
        xaxis_title="Cantidad",
        yaxis_title="",
        margin=dict(t=60, b=40, l=120),
        height=380,
    )

    st.plotly_chart(fig, width="stretch")


# ======================================================================
# Monthly Trend Chart
# ======================================================================

def _render_trend(df: pd.DataFrame) -> None:
    """Render monthly trend chart."""
    if "mes" not in df.columns or df.empty:
        st.info("No hay datos para el gráfico de tendencia.")
        return

    # Count by month and impact type
    trend = df.groupby(["mes", "tipo_impacto"]).size().reset_index(name="Cantidad")

    # Color map for impact types
    color_map = {
        "Paro de Ensamble": "#D13438",
        "Retrabajo": "#FF8C00",
        "Mejora del Proceso": "#0078D4",
        "Falta de Material": "#8764B8",
    }

    fig = go.Figure()

    for impacto in trend["tipo_impacto"].unique():
        subset = trend[trend["tipo_impacto"] == impacto].sort_values("mes")
        fig.add_trace(go.Scatter(
            x=subset["mes"],
            y=subset["Cantidad"],
            name=impacto,
            mode="lines+markers",
            line=dict(color=color_map.get(impacto, "#666"), width=2),
            marker=dict(size=7),
        ))

    # Also add total line
    total_trend = df.groupby("mes").size().reset_index(name="Cantidad").sort_values("mes")
    fig.add_trace(go.Scatter(
        x=total_trend["mes"],
        y=total_trend["Cantidad"],
        name="Total",
        mode="lines+markers",
        line=dict(color="#333", width=3, dash="dot"),
        marker=dict(size=8),
    ))

    fig.update_layout(
        title="Tendencia Mensual de Eventos",
        xaxis_title="Mes",
        yaxis_title="Cantidad de Eventos",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=60),
        height=400,
    )

    st.plotly_chart(fig, width="stretch")


# ======================================================================
# Insights
# ======================================================================

def _render_insights(df: pd.DataFrame) -> None:
    """Render insights section."""
    if df.empty:
        return

    st.subheader("💡 Insights")

    col1, col2, col3 = st.columns(3)

    # Top 3 causas
    with col1:
        st.markdown(f"""
        <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                    border-radius:{theme.border_radius}; padding:1rem; height:100%;">
            <h4 style="margin:0 0 0.5rem;">🔥 Top 3 Causas</h4>
        """, unsafe_allow_html=True)

        if "causa" in df.columns:
            top_causas = df["causa"].value_counts().head(3)
            for i, (causa, count) in enumerate(top_causas.items(), 1):
                pct = round(count / len(df) * 100, 1)
                st.markdown(f"**{i}. {causa}** — {count} eventos ({pct}%)")
        st.markdown("</div>", unsafe_allow_html=True)

    # Proyectos con más eventos
    with col2:
        st.markdown(f"""
        <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                    border-radius:{theme.border_radius}; padding:1rem; height:100%;">
            <h4 style="margin:0 0 0.5rem;">📁 Top 3 Proyectos</h4>
        """, unsafe_allow_html=True)

        if "numero_proyecto" in df.columns:
            top_proj = df["numero_proyecto"].value_counts().head(3)
            for i, (proj, count) in enumerate(top_proj.items(), 1):
                st.markdown(f"**{i}. {proj}** — {count} eventos")
        st.markdown("</div>", unsafe_allow_html=True)

    # Status summary
    with col3:
        st.markdown(f"""
        <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                    border-radius:{theme.border_radius}; padding:1rem; height:100%;">
            <h4 style="margin:0 0 0.5rem;">📊 Resumen de Status</h4>
        """, unsafe_allow_html=True)

        if "status" in df.columns:
            status_counts = df["status"].value_counts()
            total = len(df)
            for status, count in status_counts.items():
                pct = round(count / total * 100, 1)
                icon = {"Open": "🔴", "In Progress": "🟡", "Closed": "🟢"}.get(status, "⚪")
                st.markdown(f"{icon} **{status}** — {count} ({pct}%)")
        st.markdown("</div>", unsafe_allow_html=True)

    # Recommendations
    st.markdown("---")
    st.markdown(f"""
    <div style="background:#FFF8E1; border:1px solid #FFE082; border-radius:{theme.border_radius}; padding:1rem;">
        <h4 style="margin:0 0 0.5rem;">📋 Recomendaciones</h4>
    """, unsafe_allow_html=True)

    if "causa" in df.columns and "status" in df.columns:
        top_causa = df["causa"].value_counts().idxmax() if not df["causa"].value_counts().empty else None
        open_count = len(df[df["status"] == "Open"])
        total = len(df)

        if top_causa:
            causa_count = df["causa"].value_counts().iloc[0]
            st.markdown(f"- **Causa principal:** *{top_causa}* representa **{round(causa_count/total*100, 1)}%** de los eventos. Considerar plan de acción específico.")
        if open_count > 0:
            st.markdown(f"- **Eventos abiertos:** Hay **{open_count}** eventos sin cerrar ({round(open_count/total*100, 1)}%). Priorizar seguimiento.")
        if "tipo_impacto" in df.columns:
            paros = len(df[df["tipo_impacto"] == "Paro de Ensamble"])
            if paros > 0:
                st.markdown(f"- **Paros de Ensamble:** Se han registrado **{paros}** paros. Impacto directo en producción.")

    st.markdown("</div>", unsafe_allow_html=True)


# ======================================================================
# Excel Export
# ======================================================================

def _export_excel(df: pd.DataFrame) -> bytes:
    """Export DataFrame to Excel bytes."""
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Main data sheet
        export_df = df.copy()
        # Strip timezone info (Excel doesn't support tz-aware datetimes)
        for col in export_df.select_dtypes(include=["datetimetz"]).columns:
            export_df[col] = export_df[col].dt.tz_localize(None)
        # Rename columns for readability
        rename_map = {
            "id": "ID",
            "persona_detecta": "Detectó",
            "tipo_impacto": "Tipo de Impacto",
            "causa": "Causa",
            "numero_proyecto": "No. Proyecto",
            "numero_parte": "No. Parte/Plano",
            "responsable": "Responsable",
            "comentarios": "Comentarios",
            "fecha_hallazgo": "Fecha Hallazgo",
            "accion_correctiva": "Acción Correctiva",
            "accion_preventiva": "Acción Preventiva",
            "fecha_plan": "Fecha Plan",
            "fecha_real_cierre": "Fecha Real Cierre",
            "status": "Status",
        }
        export_df = export_df.rename(columns=rename_map)
        export_df.to_excel(writer, sheet_name="Eventos", index=False)

        # Summary sheet
        if "Causa" in export_df.columns:
            summary = export_df["Causa"].value_counts().reset_index()
            summary.columns = ["Causa", "Cantidad"]
            summary.to_excel(writer, sheet_name="Resumen Causas", index=False)

        if "Tipo de Impacto" in export_df.columns:
            impact_summary = export_df["Tipo de Impacto"].value_counts().reset_index()
            impact_summary.columns = ["Tipo de Impacto", "Cantidad"]
            impact_summary.to_excel(writer, sheet_name="Resumen Impacto", index=False)

        # Auto-fit columns
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column(0, 20, 18)

    return output.getvalue()


# ======================================================================
# Render Page
# ======================================================================

def render() -> None:
    """Render the reports and analysis page."""
    render_page_header(
        title="Reportes y Análisis",
        description="Análisis gráfico de eventos operativos",
        icon="📊",
    )

    # --- Toolbar ---
    col_refresh, col_export, col_spacer = st.columns([1, 1, 4])

    with col_refresh:
        refresh = st.button("🔄 Actualizar Datos", key="refresh_reports", type="secondary")

    # --- Load Data ---
    if refresh or "report_df" not in st.session_state:
        with st.spinner("Cargando datos desde SharePoint..."):
            df = _load_report_data()
            st.session_state["report_df"] = df

    df = st.session_state.get("report_df", pd.DataFrame())

    if df.empty:
        st.info("📭 No hay eventos registrados. Captura un evento primero.")
        return

    # --- Export button (needs data loaded — will use filtered df below) ---

    # --- Filters ---
    st.markdown("---")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)

    with f_col1:
        min_date = df["fecha_hallazgo"].min() if "fecha_hallazgo" in df.columns else None
        fecha_inicio = st.date_input(
            "Fecha Inicio",
            value=min_date.date() if pd.notna(min_date) else None,
            key="rpt_fecha_inicio",
        )

    with f_col2:
        max_date = df["fecha_hallazgo"].max() if "fecha_hallazgo" in df.columns else None
        fecha_fin = st.date_input(
            "Fecha Fin",
            value=max_date.date() if pd.notna(max_date) else None,
            key="rpt_fecha_fin",
        )

    with f_col3:
        proyectos = ["Todos"] + sorted(df["numero_proyecto"].dropna().unique().tolist()) if "numero_proyecto" in df.columns else ["Todos"]
        selected_proyecto = st.selectbox("Proyecto", options=proyectos, key="rpt_proyecto")

    with f_col4:
        statuses = ["Todos", "Open", "In Progress", "Closed"]
        selected_status = st.selectbox("Status", options=statuses, key="rpt_status")

    # Apply filters
    filtered = df.copy()
    # Strip timezone for date comparison (SharePoint returns UTC-aware datetimes)
    if "fecha_hallazgo" in filtered.columns and hasattr(filtered["fecha_hallazgo"].dtype, "tz"):
        filtered["fecha_hallazgo"] = filtered["fecha_hallazgo"].dt.tz_localize(None)
    if fecha_inicio and "fecha_hallazgo" in filtered.columns:
        filtered = filtered[filtered["fecha_hallazgo"] >= pd.Timestamp(fecha_inicio)]
    if fecha_fin and "fecha_hallazgo" in filtered.columns:
        filtered = filtered[filtered["fecha_hallazgo"] <= pd.Timestamp(fecha_fin) + pd.Timedelta(days=1)]
    if selected_proyecto != "Todos" and "numero_proyecto" in filtered.columns:
        filtered = filtered[filtered["numero_proyecto"] == selected_proyecto]
    if selected_status != "Todos" and "status" in filtered.columns:
        filtered = filtered[filtered["status"] == selected_status]

    filtered = filtered.reset_index(drop=True)

    # --- Export (uses filtered data) ---
    with col_export:
        excel_bytes = _export_excel(filtered)
        st.download_button(
            label="📥 Exportar Excel",
            data=excel_bytes,
            file_name="reporte_eventos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="export_excel",
        )

    if filtered.empty:
        st.warning("No hay eventos que coincidan con los filtros seleccionados.")
        return

    # --- Summary Metrics ---
    total = len(filtered)
    open_count = len(filtered[filtered["status"] == "Open"]) if "status" in filtered.columns else 0
    in_progress = len(filtered[filtered["status"] == "In Progress"]) if "status" in filtered.columns else 0
    closed = len(filtered[filtered["status"] == "Closed"]) if "status" in filtered.columns else 0

    # Avg close time (days) — for events that have both fecha_hallazgo and fecha_real_cierre
    avg_close_days = None
    if "fecha_hallazgo" in filtered.columns and "fecha_real_cierre" in filtered.columns:
        closed_events = filtered.dropna(subset=["fecha_hallazgo", "fecha_real_cierre"])
        if not closed_events.empty:
            cierre = pd.to_datetime(closed_events["fecha_real_cierre"], errors="coerce")
            hallazgo = closed_events["fecha_hallazgo"]
            deltas = (cierre - hallazgo).dt.days
            deltas = deltas.dropna()
            if len(deltas) > 0:
                avg_close_days = round(deltas.mean(), 1)

    # Close efficiency (%)
    close_efficiency = round(closed / total * 100, 1) if total > 0 else 0.0

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Eventos", total)
    m2.metric("🔴 Open", open_count)
    m3.metric("🟡 In Progress", in_progress)
    m4.metric("🟢 Closed", closed)
    m5.metric("⏱️ Prom. Cierre", f"{avg_close_days} días" if avg_close_days is not None else "N/A")
    m6.metric("✅ Eficiencia", f"{close_efficiency}%")

    st.markdown("---")

    # --- Charts: 2x2 grid ---
    # Row 1: Pareto Impacto | Eventos por Proyecto
    chart_r1c1, chart_r1c2 = st.columns(2)
    with chart_r1c1:
        _render_pareto(filtered, column="tipo_impacto", title="Pareto — Tipo de Impacto", bar_color="#D13438")
    with chart_r1c2:
        _render_events_by_project(filtered)

    # Row 2: Pareto Causas | Tendencia Mensual
    chart_r2c1, chart_r2c2 = st.columns(2)
    with chart_r2c1:
        _render_pareto(filtered, column="causa", title="Pareto — Causas", bar_color="#0078D4")
    with chart_r2c2:
        _render_trend(filtered)

    st.markdown("---")

    # --- Insights ---
    _render_insights(filtered)
