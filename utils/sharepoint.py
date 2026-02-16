"""
============================================================================
SharePoint / Microsoft Lists — CRUD Operations
============================================================================
Functions to create, read, update items in a Microsoft List via MS Graph API.
Used as the persistence layer for Operation Events (RF-001, RF-002).

Requirements:
    - Azure AD app registration with Sites.ReadWrite.All application permission
    - Admin consent granted in Azure Portal
    - SHAREPOINT_SITE_ID and SHAREPOINT_LIST_ID set in .env

Usage:
    from utils.sharepoint import create_event, get_all_events, update_event

    # Create a new event
    item_id = create_event({
        "PersonaDetecta": "John Doe",
        "TipoImpacto": "Paro de Ensamble",
        "Causa": "Falla de equipo",
        ...
    })

    # Read all events
    events = get_all_events()

    # Update an event
    update_event(item_id, {"Status": "Closed"})
============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import msal
import requests
import streamlit as st

from config.settings import get_settings


# ======================================================================
# Graph API Endpoints
# ======================================================================

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def _get_list_items_url() -> str:
    """Build the Graph API URL for list items."""
    s = get_settings()
    return f"{GRAPH_BASE}/sites/{s.sharepoint_site_id}/lists/{s.sharepoint_list_id}/items"


def _get_list_item_url(item_id: str) -> str:
    """Build the Graph API URL for a specific list item."""
    return f"{_get_list_items_url()}/{item_id}"


# ======================================================================
# Authentication — Client Credentials
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
    """
    Acquire an application-level access token using client credentials.
    Returns the access token string, or None on failure.
    """
    app = _get_msal_app()
    result = app.acquire_token_for_client(
        scopes=get_settings().graph_app_scopes,
    )
    if "access_token" in result:
        return result["access_token"]
    return None


def _get_headers() -> dict[str, str] | None:
    """Build authorization headers. Returns None if token unavailable."""
    token = _get_app_token()
    if not token:
        return None
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


# ======================================================================
# Field Mapping: Python dict keys → SharePoint column internal names
# ======================================================================
# SharePoint List columns must be created with these internal names.
# You can adjust the mapping if your column names differ.

FIELD_MAP = {
    "persona_detecta":   "field_6",          # PersonaDetecta
    "tipo_impacto":      "field_7",          # Tipo de Impacto
    "causa":             "field_10",         # Tipo de Retrabajo (= Causa)
    "numero_proyecto":   "field_8",          # Numero de Proyecto
    "numero_parte":      "field_9",          # Numero_Parte_Numero de Plano
    "responsable":       "field_12",         # Responsable
    "comentarios":       "field_11",         # Question (= Comentarios)
    "fecha_hallazgo":    "field_14",         # Fecha de Hallazgo
    "accion_correctiva": "AccionCorrectiva", # Accion Correctiva
    "accion_preventiva": "AccionPreventiva", # Accion Preventiva
    "fecha_plan":        "FechaPlan",        # Fecha Plan
    "fecha_real_cierre": "FechaReal",        # Fecha Real
    "status":            "Status",           # Status
}


def _to_sharepoint_fields(data: dict[str, Any]) -> dict[str, Any]:
    """Convert Python-style keys to SharePoint column names."""
    fields: dict[str, Any] = {}
    for py_key, sp_key in FIELD_MAP.items():
        if py_key in data:
            val = data[py_key]
            # Convert datetime to ISO string for SharePoint
            if isinstance(val, datetime):
                val = val.isoformat()
            if val is not None:
                fields[sp_key] = val
    return fields


def _from_sharepoint_fields(item: dict[str, Any]) -> dict[str, Any]:
    """Convert a SharePoint list item to a Python dict with friendly keys."""
    fields = item.get("fields", {})
    result: dict[str, Any] = {"id": item.get("id", "")}
    reverse_map = {v: k for k, v in FIELD_MAP.items()}
    for sp_key, value in fields.items():
        py_key = reverse_map.get(sp_key, sp_key)
        result[py_key] = value
    return result


# ======================================================================
# CRUD Operations
# ======================================================================

def create_event(data: dict[str, Any]) -> str | None:
    """
    Create a new event in the Microsoft List.

    Args:
        data: Dict with Python-style keys (e.g. persona_detecta, tipo_impacto).

    Returns:
        The created item's ID, or None on failure.
    """
    headers = _get_headers()
    if not headers:
        st.error("No se pudo obtener token de acceso. Verifica la configuración de Azure AD.")
        return None

    sp_fields = _to_sharepoint_fields(data)
    payload = {"fields": sp_fields}

    try:
        resp = requests.post(
            _get_list_items_url(),
            headers=headers,
            json=payload,
            timeout=15,
        )
        if resp.ok:
            return resp.json().get("id")
        else:
            error_msg = resp.json().get("error", {}).get("message", resp.text)
            st.error(f"Error al crear evento en SharePoint: {error_msg}")
            return None
    except Exception as e:
        st.error(f"Error de conexión con SharePoint: {e}")
        return None


def get_all_events(
    select_fields: list[str] | None = None,
    expand: bool = True,
) -> list[dict[str, Any]]:
    """
    Fetch all events from the Microsoft List.

    Args:
        select_fields: Optional list of SharePoint column names to select.
        expand: Whether to expand fields (default True).

    Returns:
        List of event dicts with Python-style keys.
    """
    headers = _get_headers()
    if not headers:
        st.error("No se pudo obtener token de acceso. Verifica la configuración de Azure AD.")
        return []

    params: dict[str, str] = {}
    if expand:
        if select_fields:
            fields_str = ",".join(select_fields)
            params["$expand"] = f"fields($select={fields_str})"
        else:
            params["$expand"] = "fields"
    params["$top"] = "999"

    all_items: list[dict[str, Any]] = []

    try:
        url: str | None = _get_list_items_url()
        while url:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            if not resp.ok:
                error_msg = resp.json().get("error", {}).get("message", resp.text)
                st.error(f"Error al leer eventos de SharePoint: {error_msg}")
                return all_items

            data = resp.json()
            items = data.get("value", [])
            all_items.extend([_from_sharepoint_fields(item) for item in items])

            # Pagination
            url = data.get("@odata.nextLink")
            params = {}  # nextLink already contains params

    except Exception as e:
        st.error(f"Error de conexión con SharePoint: {e}")

    return all_items


def update_event(item_id: str, data: dict[str, Any]) -> bool:
    """
    Update an existing event in the Microsoft List.

    Args:
        item_id: The SharePoint list item ID.
        data: Dict with Python-style keys for fields to update.

    Returns:
        True if update succeeded, False otherwise.
    """
    headers = _get_headers()
    if not headers:
        st.error("No se pudo obtener token de acceso. Verifica la configuración de Azure AD.")
        return False

    sp_fields = _to_sharepoint_fields(data)
    url = f"{_get_list_item_url(item_id)}/fields"

    try:
        resp = requests.patch(
            url,
            headers=headers,
            json=sp_fields,
            timeout=15,
        )
        if resp.ok:
            return True
        else:
            error_msg = resp.json().get("error", {}).get("message", resp.text)
            st.error(f"Error al actualizar evento en SharePoint: {error_msg}")
            return False
    except Exception as e:
        st.error(f"Error de conexión con SharePoint: {e}")
        return False


def get_list_columns() -> tuple[bool, list[dict[str, str]], str]:
    """
    Fetch column definitions from the Microsoft List.

    Returns:
        Tuple of (success, columns_list, error_message).
        Each column dict has keys: name, displayName, type.
    """
    headers = _get_headers()
    if not headers:
        return False, [], "No se pudo obtener token de acceso."

    s = get_settings()
    if not s.sharepoint_site_id or not s.sharepoint_list_id:
        return False, [], "SHAREPOINT_SITE_ID o SHAREPOINT_LIST_ID no configurados."

    url = f"{GRAPH_BASE}/sites/{s.sharepoint_site_id}/lists/{s.sharepoint_list_id}/columns"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.ok:
            raw_columns = resp.json().get("value", [])
            columns = [
                {
                    "name": col.get("name", ""),
                    "displayName": col.get("displayName", ""),
                    "type": col.get("text", col.get("dateTime", col.get("choice", col.get("number", {})))),
                    "description": col.get("description", ""),
                    "columnType": _resolve_column_type(col),
                }
                for col in raw_columns
                if not col.get("hidden", False) and not col.get("readOnly", False)
            ]
            return True, columns, ""
        else:
            error_msg = resp.json().get("error", {}).get("message", resp.text)
            return False, [], f"Error: {error_msg}"
    except Exception as e:
        return False, [], f"Error de conexión: {e}"


def _resolve_column_type(col: dict) -> str:
    """Resolve the column type from Graph API column definition."""
    if "text" in col:
        return "Text"
    if "dateTime" in col:
        return "DateTime"
    if "choice" in col:
        return "Choice"
    if "number" in col:
        return "Number"
    if "boolean" in col:
        return "Boolean"
    if "personOrGroup" in col:
        return "Person"
    if "lookup" in col:
        return "Lookup"
    return col.get("type", "Unknown")


def test_sharepoint_connection() -> tuple[bool, str]:
    """
    Test the connection to SharePoint by attempting to read the list metadata.

    Returns:
        Tuple of (success: bool, message: str).
    """
    headers = _get_headers()
    if not headers:
        return False, "No se pudo obtener token de acceso. Verifica las credenciales de Azure AD."

    s = get_settings()
    if not s.sharepoint_site_id or not s.sharepoint_list_id:
        return False, "SHAREPOINT_SITE_ID o SHAREPOINT_LIST_ID no están configurados en .env"

    url = f"{GRAPH_BASE}/sites/{s.sharepoint_site_id}/lists/{s.sharepoint_list_id}"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.ok:
            list_name = resp.json().get("displayName", "Unknown")
            return True, f"Conexión exitosa. Lista: '{list_name}'"
        else:
            error_msg = resp.json().get("error", {}).get("message", resp.text)
            return False, f"Error: {error_msg}"
    except Exception as e:
        return False, f"Error de conexión: {e}"
