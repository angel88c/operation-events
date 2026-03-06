"""
============================================================================
Email Notifications — MS Graph API
============================================================================
Send email notifications to event responsables when a new event is captured.
Uses Microsoft Graph API with application-level (client credentials) auth.

Requirements:
    - Azure AD app with Mail.Send application permission
    - Admin consent granted
    - EMAIL_SENDER configured in .env

Referencia: specs/operation-events.md — Milestone 2
============================================================================
"""

from __future__ import annotations

from typing import Any

import msal
import requests
import streamlit as st

from config.settings import get_settings


# ======================================================================
# Graph API Endpoints
# ======================================================================

GRAPH_SEND_MAIL = "https://graph.microsoft.com/v1.0/users/{sender}/sendMail"


# ======================================================================
# Authentication — reuse MSAL app from sharepoint module
# ======================================================================

@st.cache_resource(ttl=3000, show_spinner=False)
def _get_msal_app() -> msal.ConfidentialClientApplication:
    """Cached MSAL confidential client for app-level operations."""
    s = get_settings()
    return msal.ConfidentialClientApplication(
        client_id=s.azure_client_id,
        client_credential=s.azure_client_secret,
        authority=s.azure_authority,
    )


def _get_app_token() -> str | None:
    """Acquire an application-level access token."""
    app = _get_msal_app()
    result = app.acquire_token_for_client(
        scopes=get_settings().graph_app_scopes,
    )
    if "access_token" in result:
        return result["access_token"]
    return None


# ======================================================================
# Email Template
# ======================================================================

def _build_email_html(event_data: dict[str, Any]) -> str:
    """Build a professional HTML email body with event details."""
    settings = get_settings()
    app_url = settings.app_url or "http://localhost:3001"

    persona = event_data.get("persona_detecta", "N/A")
    tipo_impacto = event_data.get("tipo_impacto", "N/A")
    causa = event_data.get("causa", "N/A")
    numero_proyecto = event_data.get("numero_proyecto", "N/A")
    numero_parte = event_data.get("numero_parte", "N/A")
    responsable = event_data.get("responsable", "N/A")
    comentarios = event_data.get("comentarios", "—")
    fecha = event_data.get("fecha_hallazgo", "N/A")
    if hasattr(fecha, "strftime"):
        fecha = fecha.strftime("%d/%m/%Y %H:%M")

    # Color based on impact type
    impact_colors = {
        "Paro de Ensamble": "#D13438",
        "Retrabajo": "#FF8C00",
        "Mejora del Proceso": "#0078D4",
        "Falta de Material": "#8764B8",
    }
    accent_color = impact_colors.get(tipo_impacto, "#0078D4")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; padding:0; font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif; background:#f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5; padding:20px 0;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

                        <!-- Header -->
                        <tr>
                            <td style="background:{accent_color}; padding:24px 32px;">
                                <h1 style="color:#ffffff; margin:0; font-size:20px; font-weight:600;">
                                    Nuevo Evento Operativo
                                </h1>
                                <p style="color:rgba(255,255,255,0.85); margin:6px 0 0; font-size:14px;">
                                    Se te ha asignado como responsable de un evento
                                </p>
                            </td>
                        </tr>

                        <!-- Impact Badge -->
                        <tr>
                            <td style="padding:24px 32px 0;">
                                <table cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="background:{accent_color}; color:#fff; padding:6px 16px; border-radius:4px; font-size:13px; font-weight:600;">
                                            {tipo_impacto}
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- Event Details -->
                        <tr>
                            <td style="padding:20px 32px;">
                                <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e0e0e0; border-radius:6px; overflow:hidden;">
                                    <tr style="background:#fafafa;">
                                        <td style="padding:10px 16px; font-size:13px; color:#666; width:40%; border-bottom:1px solid #e0e0e0;">Causa</td>
                                        <td style="padding:10px 16px; font-size:13px; color:#333; border-bottom:1px solid #e0e0e0; font-weight:500;">{causa}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:10px 16px; font-size:13px; color:#666; border-bottom:1px solid #e0e0e0;">No. Proyecto</td>
                                        <td style="padding:10px 16px; font-size:13px; color:#333; border-bottom:1px solid #e0e0e0; font-weight:500;">{numero_proyecto}</td>
                                    </tr>
                                    <tr style="background:#fafafa;">
                                        <td style="padding:10px 16px; font-size:13px; color:#666; border-bottom:1px solid #e0e0e0;">No. Parte / Plano</td>
                                        <td style="padding:10px 16px; font-size:13px; color:#333; border-bottom:1px solid #e0e0e0; font-weight:500;">{numero_parte}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:10px 16px; font-size:13px; color:#666; border-bottom:1px solid #e0e0e0;">Detectado por</td>
                                        <td style="padding:10px 16px; font-size:13px; color:#333; border-bottom:1px solid #e0e0e0; font-weight:500;">{persona}</td>
                                    </tr>
                                    <tr style="background:#fafafa;">
                                        <td style="padding:10px 16px; font-size:13px; color:#666; border-bottom:1px solid #e0e0e0;">Responsable</td>
                                        <td style="padding:10px 16px; font-size:13px; color:#333; border-bottom:1px solid #e0e0e0; font-weight:600;">{responsable}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:10px 16px; font-size:13px; color:#666; border-bottom:1px solid #e0e0e0;">Fecha</td>
                                        <td style="padding:10px 16px; font-size:13px; color:#333; border-bottom:1px solid #e0e0e0;">{fecha}</td>
                                    </tr>
                                    <tr style="background:#fafafa;">
                                        <td style="padding:10px 16px; font-size:13px; color:#666;">Comentarios</td>
                                        <td style="padding:10px 16px; font-size:13px; color:#333;">{comentarios if comentarios else '—'}</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- CTA Button -->
                        <tr>
                            <td style="padding:8px 32px 28px;" align="center">
                                <a href="{app_url}" style="display:inline-block; background:{accent_color}; color:#ffffff; text-decoration:none; padding:12px 32px; border-radius:6px; font-size:14px; font-weight:600;">
                                    Abrir Operation Events
                                </a>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="background:#fafafa; padding:16px 32px; border-top:1px solid #e0e0e0;">
                                <p style="margin:0; font-size:12px; color:#999; text-align:center;">
                                    Este es un mensaje automático de Operation Events. No responder a este correo.
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


# ======================================================================
# Send Email
# ======================================================================

def send_event_notification(
    event_data: dict[str, Any],
    recipient_email: str,
    recipient_name: str = "",
) -> tuple[bool, str]:
    """
    Send an email notification to the event responsable.

    Args:
        event_data: Dict with event fields (persona_detecta, tipo_impacto, etc.)
        recipient_email: Email address of the responsable.
        recipient_name: Display name of the responsable.

    Returns:
        Tuple of (success: bool, message: str).
    """
    settings = get_settings()

    if not settings.email_sender:
        return False, "EMAIL_SENDER no está configurado en .env"

    token = _get_app_token()
    if not token:
        return False, "No se pudo obtener token de acceso para enviar email."

    tipo_impacto = event_data.get("tipo_impacto", "Evento")
    numero_proyecto = event_data.get("numero_proyecto", "")
    subject = f"[Operation Events] {tipo_impacto} — Proyecto {numero_proyecto}"

    html_body = _build_email_html(event_data)

    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": html_body,
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient_email,
                        "name": recipient_name or recipient_email,
                    }
                }
            ],
        },
        "saveToSentItems": "false",
    }

    url = GRAPH_SEND_MAIL.format(sender=settings.email_sender)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 202:
            return True, f"Email enviado a {recipient_email}"
        else:
            error_msg = resp.json().get("error", {}).get("message", resp.text)
            return False, f"Error al enviar email: {error_msg}"
    except Exception as e:
        return False, f"Error de conexión al enviar email: {e}"
