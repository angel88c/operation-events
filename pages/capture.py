"""
============================================================================
Pantalla de Captura de Eventos Operativos (RF-001)
============================================================================
Formulario para registrar un nuevo evento operativo detectado en producción.
Al enviar, guarda en Microsoft List y envía email al responsable.

Campos:
    - Persona que detecta hallazgo (selector M365)
    - Tipo de Impacto (selector catálogo)
    - Causa (selector dinámico filtrado por Impacto)
    - Número de Proyecto (texto, max 10 chars)
    - Número de Parte / Número de Plano (texto, max 15 chars)
    - Responsable (selector M365)
    - Comentarios adicionales (textarea, max 300 chars)
    - Fecha de Hallazgo (automática)

Referencia: specs/operation-events.md — RF-001
============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import streamlit as st

from auth.graph_users import render_user_select
from auth.microsoft import get_current_user
from components.navigation import render_page_header
from config.catalogs import get_impact_types, get_causes_for_impact
from config.settings import get_settings
from config.theme import theme
from utils.email import send_event_notification
from utils.sharepoint import create_event


def render() -> None:
    """Render the event capture page."""
    render_page_header(
        title="Captura de Datos Básicos",
        description="Registre un nuevo evento operativo detectado",
        icon="➕",
    )

    # Gradient divider
    st.markdown(
        f"""
        <div style="height:4px; border-radius:2px; margin-bottom:1.5rem;
                    background: linear-gradient(90deg, {theme.colors.primary}, {theme.colors.primary_light});"></div>
        """,
        unsafe_allow_html=True,
    )

    settings = get_settings()
    domain = settings.user_domain

    # ── Form container ──────────────────────────────────────────────
    with st.container():
        st.markdown(
            f"""
            <div style="background:{theme.colors.surface}; border:1px solid {theme.colors.border};
                        border-radius:{theme.border_radius}; padding:0.5rem; margin-bottom:0.5rem;">
            """,
            unsafe_allow_html=True,
        )

        # Row 1: Persona que detecta | Tipo de Impacto
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🪪 Persona que detecta hallazgo (Usuario Actual)**")
            persona = get_current_user()
            st.text_input(label="Empty", label_visibility="hidden", value=f"{persona.get('name', 'N/A')} ({persona.get('email', 'N/A')})", disabled=True)
            # st.text(f"{persona.get('name', 'N/A')} ({persona.get('email', 'N/A')})")
            # persona = render_user_select(
            #     domain=domain,
            #     label="Seleccione una persona...",
            #     key="capture_persona_detecta",
            #     disabled=True,
            #     #include_email=True,
            # )

        with col2:
            st.markdown("**Tipo de Impacto**")
            impact_types = get_impact_types()
            tipo_impacto = st.selectbox(
                label="Seleccione tipo de impacto...",
                options=[""] + impact_types,
                key="capture_tipo_impacto",
                label_visibility="visible",
            )

        # Row 2: Causa | Número de Proyecto
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**🔍 Causa**")
            if tipo_impacto:
                causas = get_causes_for_impact(tipo_impacto)
                causa = st.selectbox(
                    "Seleccione causa...",
                    options=[""] + causas,
                    key="capture_causa",
                    label_visibility="collapsed",
                )
            else:
                st.selectbox(
                    "Primero seleccione tipo de impacto...",
                    options=["Primero seleccione tipo de impacto..."],
                    disabled=True,
                    key="capture_causa_disabled",
                    label_visibility="collapsed",
                )
                causa = ""

        with col4:
            st.markdown("**📁 Número de Proyecto**")
            numero_proyecto = st.text_input(
                "Máximo 10 caracteres",
                max_chars=10,
                key="capture_numero_proyecto",
                label_visibility="collapsed",
                placeholder="Máximo 10 caracteres",
            )

        # Row 3: Número de Parte | Responsable
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("**🏷️ Número de Parte / Número de Plano**")
            numero_parte = st.text_input(
                label="Escriba el número de parte o plano",
                max_chars=15,
                key="capture_numero_parte",
                label_visibility="visible",
                placeholder="Máximo 15 caracteres",
            )

        with col6:
            st.markdown("**👤 Responsable**")
            responsable = render_user_select(
                domain=domain,
                label="Seleccione un responsable...",
                key="capture_responsable",
                include_email=True,
            )

        # Row 4: Comentarios adicionales (full width)
        st.markdown("**💬 Comentarios adicionales**")
        comentarios = st.text_area(
            "Máximo 300 caracteres",
            max_chars=300,
            key="capture_comentarios",
            label_visibility="collapsed",
            placeholder="Máximo 300 caracteres",
            height=120,
        )
        # Character counter
        char_count = len(comentarios) if comentarios else 0
        counter_color = theme.colors.danger if char_count >= 280 else theme.colors.text_muted
        st.markdown(
            f'<span style="font-size:0.8rem; color:{counter_color};">'
            f'{char_count}/300 caracteres</span>',
            unsafe_allow_html=True,
        )

        # Row 5: Fecha de Hallazgo (auto)
        now = datetime.now()
        st.markdown("**📅 Fecha de Hallazgo**")
        st.markdown(
            f'<span style="font-size:1rem; color:{theme.colors.text_primary};">'
            f'{now.strftime("%d/%m/%Y, %H:%M:%S")}</span>',
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Submit button ───────────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    col_btn_l, col_btn_c, col_btn_r = st.columns([1, 2, 1])
    with col_btn_c:
        submitted = st.button(
            "✈️ Enviar y Guardar",
            type="primary",
            use_container_width=True,
            key="capture_submit",
        )

    # ── Validation & Save ───────────────────────────────────────────
    if submitted:
        errors = _validate_form(
            persona=persona,
            tipo_impacto=tipo_impacto,
            causa=causa,
            numero_proyecto=numero_proyecto,
            numero_parte=numero_parte,
            responsable=responsable,
        )

        if errors:
            for err in errors:
                st.error(err)
        else:
            _save_event(
                persona=persona,
                tipo_impacto=tipo_impacto,
                causa=causa,
                numero_proyecto=numero_proyecto,
                numero_parte=numero_parte,
                responsable=responsable,
                comentarios=comentarios,
                fecha_hallazgo=now,
            )


# ======================================================================
# Validation
# ======================================================================

def _validate_form(
    persona: dict[str, Any] | None,
    tipo_impacto: str,
    causa: str,
    numero_proyecto: str,
    numero_parte: str,
    responsable: dict[str, Any] | None,
) -> list[str]:
    """Validate all required fields. Returns list of error messages."""
    errors: list[str] = []

    if not persona:
        errors.append("**Persona que detecta hallazgo** es obligatorio.")
    if not tipo_impacto:
        errors.append("**Tipo de Impacto** es obligatorio.")
    if not causa:
        errors.append("**Causa** es obligatoria.")
    if not numero_proyecto or not numero_proyecto.strip():
        errors.append("**Número de Proyecto** es obligatorio.")
    if not numero_parte or not numero_parte.strip():
        errors.append("**Número de Parte / Número de Plano** es obligatorio.")
    if not responsable:
        errors.append("**Responsable** es obligatorio.")

    return errors


# ======================================================================
# Save Event
# ======================================================================

def _save_event(
    persona: dict[str, Any],
    tipo_impacto: str,
    causa: str,
    numero_proyecto: str,
    numero_parte: str,
    responsable: dict[str, Any],
    comentarios: str,
    fecha_hallazgo: datetime,
) -> None:
    """Save the event to Microsoft List and show confirmation."""
    persona_name = persona.get("name") or persona.get("displayName", "")
    responsable_name = responsable.get("displayName", "")
    responsable_email = responsable.get("mail") or responsable.get("userPrincipalName", "")

    event_data = {
        "persona_detecta": persona_name,
        "tipo_impacto": tipo_impacto,
        "causa": causa,
        "numero_proyecto": numero_proyecto.strip(),
        "numero_parte": numero_parte.strip(),
        "responsable": responsable_name,
        "comentarios": comentarios.strip() if comentarios else "",
        "fecha_hallazgo": fecha_hallazgo,
        "status": "Open",
    }

    with st.spinner("Guardando evento..."):
        item_id = create_event(event_data)

    if item_id:
        st.success(f"✅ Evento registrado exitosamente (ID: {item_id}).")

        # Send email notification to responsable
        if responsable_email:
            with st.spinner(f"Enviando notificación a {responsable_email}..."):
                email_ok, email_msg = send_event_notification(
                    event_data=event_data,
                    recipient_email=responsable_email,
                    recipient_name=responsable_name,
                )
            if email_ok:
                st.success(f"📧 {email_msg}")
            else:
                st.warning(f"⚠️ Evento guardado pero no se pudo enviar email: {email_msg}")
        else:
            st.warning("⚠️ Evento guardado pero no se encontró email del responsable.")

        st.session_state["last_saved_event"] = {
            **event_data,
            "id": item_id,
        }
    else:
        st.error("❌ No se pudo guardar el evento. Revisa la conexión con SharePoint.")
