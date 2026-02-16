"""
============================================================================
Pantalla de Configuración (RF-004)
============================================================================
Configuración de la aplicación: prueba de conexión a SharePoint,
catálogos de Tipo de Impacto y Causas asociadas.

Referencia: specs/operation-events.md — RF-004, Milestone 5
============================================================================
"""

from __future__ import annotations

import streamlit as st

from auth.microsoft import is_authenticated, get_current_user
from components.navigation import render_page_header
from config.catalogs import get_catalog, get_impact_types, get_causes_for_impact
from config.settings import get_settings
from config.theme import theme
from utils.sharepoint import test_sharepoint_connection, get_list_columns, FIELD_MAP


def render() -> None:
    """Render the Configuration page."""
    render_page_header(
        title="Configuración",
        description="Administración de conexiones y catálogos del sistema",
        icon="⚙️",
    )

    tab1, tab2, tab3 = st.tabs([
        "🔗 Conexión SharePoint",
        "📋 Catálogos",
        "👤 Perfil de Usuario",
    ])

    # ================================================================
    # Tab 1: SharePoint Connection Test
    # ================================================================
    with tab1:
        st.subheader("Prueba de Conexión a SharePoint")

        settings = get_settings()

        # Show current config (masked)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**SharePoint Site ID:**")
            site_display = (settings.sharepoint_site_id[:20] + "…") if settings.sharepoint_site_id else "❌ No configurado"
            st.code(site_display, language=None)
        with col2:
            st.markdown("**SharePoint List ID:**")
            list_display = (settings.sharepoint_list_id[:20] + "…") if settings.sharepoint_list_id else "❌ No configurado"
            st.code(list_display, language=None)

        st.markdown("")

        if st.button("🔄 Probar Conexión", type="primary", key="test_sp_connection"):
            with st.spinner("Probando conexión con SharePoint..."):
                success, message = test_sharepoint_connection()

            if success:
                st.success(f"✅ {message}")

                # Fetch and display list columns
                col_ok, columns, col_err = get_list_columns()
                if col_ok and columns:
                    st.markdown("---")
                    st.subheader("Columnas de la Lista")

                    expected_cols = set(FIELD_MAP.values())
                    actual_col_names = {c["name"] for c in columns}

                    # Show columns table
                    for col in columns:
                        name = col["name"]
                        display = col["displayName"]
                        col_type = col["columnType"]
                        is_mapped = "✅" if name in expected_cols else ""
                        st.markdown(f"- **{display}** (`{name}`) — _{col_type}_ {is_mapped}")

                    # Show missing columns
                    missing = expected_cols - actual_col_names
                    if missing:
                        st.markdown("---")
                        st.warning(
                            f"⚠️ **Columnas faltantes en SharePoint** (requeridas por la app):\n\n"
                            + "\n".join(f"- `{m}`" for m in sorted(missing))
                        )
                    else:
                        st.success("✅ Todas las columnas requeridas por la app existen en la lista.")
                elif col_err:
                    st.warning(f"No se pudieron obtener las columnas: {col_err}")
            else:
                st.error(f"❌ {message}")

        st.markdown(
            f"""
            <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                        border-radius:{theme.border_radius}; padding:1rem; margin-top:1rem;">
                <p style="color:{theme.colors.text_muted}; font-size:0.85rem; margin:0;">
                    💡 <strong>Tip:</strong> Configura <code>SHAREPOINT_SITE_ID</code> y
                    <code>SHAREPOINT_LIST_ID</code> en tu archivo <code>.env</code>.
                    Consulta <code>.env.example</code> para instrucciones de cómo obtener estos valores.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ================================================================
    # Tab 2: Catalogs Viewer
    # ================================================================
    with tab2:
        st.subheader("Catálogos de Tipo de Impacto y Causas")

        st.markdown(
            f"""
            <div style="background:{theme.colors.primary_light}; border-left:4px solid {theme.colors.primary};
                        border-radius:0 {theme.border_radius} {theme.border_radius} 0;
                        padding:0.75rem 1rem; margin-bottom:1rem;">
                <p style="color:{theme.colors.text_primary}; font-size:0.9rem; margin:0;">
                    ℹ️ La edición completa de catálogos estará disponible en el <strong>Milestone 5</strong>.
                    Por ahora puedes consultar los catálogos configurados.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        catalog = get_catalog()

        for impact_type in get_impact_types():
            causes = get_causes_for_impact(impact_type)
            with st.expander(f"**{impact_type}** ({len(causes)} causas)", expanded=False):
                for i, cause in enumerate(causes, 1):
                    st.markdown(f"{i}. {cause}")

        # Summary
        total_causes = sum(len(v) for v in catalog.values())
        st.markdown(
            f"""
            <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                        border-radius:{theme.border_radius}; padding:1rem; margin-top:1rem;
                        text-align:center;">
                <span style="color:{theme.colors.text_secondary}; font-size:0.9rem;">
                    <strong>{len(catalog)}</strong> tipos de impacto &nbsp;|&nbsp;
                    <strong>{total_causes}</strong> causas totales
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ================================================================
    # Tab 3: User Profile
    # ================================================================
    with tab3:
        st.subheader("Usuario Actual")

        user = get_current_user()
        settings = get_settings()

        col1, col2 = st.columns([1, 3])
        with col1:
            photo = user.get("photo")
            if photo:
                st.markdown(
                    f"""
                    <img src="{photo}" style="
                        width:80px; height:80px; border-radius:50%;
                        object-fit:cover; border:2px solid {theme.colors.primary};
                        display:block;
                    " />
                    """,
                    unsafe_allow_html=True,
                )
            else:
                initials = "".join(
                    [w[0] for w in user.get("name", "U").split()[:2]]
                ).upper()
                st.markdown(
                    f"""
                    <div style="
                        width:80px; height:80px; border-radius:50%;
                        background:linear-gradient(135deg, {theme.colors.primary}, {theme.colors.primary_dark});
                        color:white; display:flex; align-items:center;
                        justify-content:center; font-size:1.5rem; font-weight:700;
                    ">
                        {initials}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown(f"**Nombre:** {user.get('name', 'N/A')}")
            st.markdown(f"**Email:** {user.get('email', 'N/A')}")
            st.markdown(f"**Puesto:** {user.get('job_title', 'N/A')}")
            auth_status = "✅ Autenticado" if is_authenticated() else "🔓 Modo Desarrollo"
            st.markdown(f"**Estado:** {auth_status}")

        st.markdown("---")
        st.subheader("Información del Sistema")

        sys_data = {
            "Aplicación": settings.app_name,
            "Versión": settings.app_version,
            "Entorno": settings.app_env,
            "Autenticación": "Habilitada" if settings.enable_auth else "Deshabilitada",
        }

        for label, value in sys_data.items():
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"**{label}**")
            with c2:
                st.code(value, language=None)
