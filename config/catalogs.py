"""
============================================================================
Catálogos de Impacto y Causa — Operation Events
============================================================================
Catálogos configurables de Tipos de Impacto y sus Causas asociadas.
Estos catálogos se usan en la pantalla de Captura (RF-001) y se pueden
administrar desde la pantalla de Configuración (RF-004).

Persistence: catálogos se guardan en ``config/catalogs.json``.
Si el archivo no existe, se inicializa desde DEFAULT_IMPACT_CAUSE_CATALOG.

Referencia: specs/operation-events.md — Sección 11
============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# ======================================================================
# Paths
# ======================================================================

_CATALOG_DIR = Path(__file__).parent
_CATALOG_FILE = _CATALOG_DIR / "catalogs.json"


# ======================================================================
# Catálogo por defecto: Tipo de Impacto → Lista de Causas
# ======================================================================

DEFAULT_IMPACT_CAUSE_CATALOG: dict[str, list[str]] = {
    "Paro de Ensamble": [
        "Falla de equipo",
        "Falta de material",
        "Material incorrecto",
        "Material en hold de calidad",
        "Instrucción de trabajo incorrecta / no disponible",
        "Falta de Personal",
        "Personal no capacitado",
        "Ausentismo",
        "Retraso en surtido interno",
        "Defecto detectado en Máquina",
        "Contención activa",
        "Cambio urgente de prioridad",
    ],
    "Retrabajo": [
        "Defecto de material",
        "Especificación incorrecta",
        "Instrucción de trabajo no clara",
        "Método no estandarizado",
        "Error de ensamble",
        "Falta de capacitación",
        "Cambio Eng no implementado",
        "Criterio de aceptación incorrecto",
        "Defecto de proveedor",
    ],
    "Mejora del Proceso": [
        "Tiempo ciclo alto",
        "Cuello de botella",
        "Alta tasa de defectos",
        "Variabilidad del proceso",
        "Riesgo ergonómico",
        "Riesgo de accidente",
        "Scrap elevado",
        "Uso excesivo de consumibles",
        "Exceso de movimiento",
        "Layout ineficiente",
        "Proceso no estandarizado",
        "Secuencia ineficiente",
        "Falta de trazabilidad",
        "Registro manual",
        "Abasto ineficiente",
        "Inventario innecesario",
    ],
    "Falta de Material": [
        "Error en MRP",
        "Demanda mayor al forecast",
        "Inventario incorrecto en sistema",
        "Ubicación incorrecta",
        "Error de surtido",
        "Proveedor on hold",
        "Retraso de proveedor",
        "Entrega incompleta",
        "Problema de capacidad",
        "Material on hold",
        "Rechazo de lote",
        "Cambio de PN sin stock",
        "Retraso en transporte",
    ],
}


# ======================================================================
# Runtime catalog (mutable copy used by the app)
# ======================================================================

_catalog: dict[str, list[str]] | None = None


def _load_from_file() -> dict[str, list[str]] | None:
    """Load catalog from JSON file if it exists."""
    if _CATALOG_FILE.exists():
        try:
            with open(_CATALOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
    return None


def _save_to_file(catalog: dict[str, list[str]]) -> bool:
    """Persist catalog to JSON file. Returns True on success."""
    try:
        with open(_CATALOG_FILE, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def get_catalog() -> dict[str, list[str]]:
    """
    Return the current impact→cause catalog.
    Load order: runtime cache → JSON file → defaults.
    """
    global _catalog
    if _catalog is None:
        loaded = _load_from_file()
        if loaded is not None:
            _catalog = loaded
        else:
            _catalog = {k: list(v) for k, v in DEFAULT_IMPACT_CAUSE_CATALOG.items()}
            _save_to_file(_catalog)
    return _catalog


def get_impact_types() -> list[str]:
    """Return the list of available impact types."""
    return list(get_catalog().keys())


def get_causes_for_impact(impact_type: str) -> list[str]:
    """Return the list of causes associated with a given impact type."""
    return get_catalog().get(impact_type, [])


# ======================================================================
# CRUD — Impact Types
# ======================================================================

def add_impact_type(name: str) -> bool:
    """Add a new impact type with an empty cause list. Returns False if it already exists."""
    catalog = get_catalog()
    if name in catalog:
        return False
    catalog[name] = []
    _save_to_file(catalog)
    return True


def rename_impact_type(old_name: str, new_name: str) -> bool:
    """Rename an impact type, preserving its causes and order."""
    catalog = get_catalog()
    if old_name not in catalog or new_name in catalog:
        return False
    # Preserve order
    new_catalog: dict[str, list[str]] = {}
    for key, val in catalog.items():
        if key == old_name:
            new_catalog[new_name] = val
        else:
            new_catalog[key] = val
    _catalog_replace(new_catalog)
    return True


def remove_impact_type(name: str) -> bool:
    """Remove an impact type and all its causes."""
    catalog = get_catalog()
    if name not in catalog:
        return False
    del catalog[name]
    _save_to_file(catalog)
    return True


# ======================================================================
# CRUD — Causes
# ======================================================================

def add_cause(impact_type: str, cause: str) -> bool:
    """Add a cause to an impact type. Returns False if duplicate or type not found."""
    catalog = get_catalog()
    if impact_type not in catalog:
        return False
    if cause in catalog[impact_type]:
        return False
    catalog[impact_type].append(cause)
    _save_to_file(catalog)
    return True


def remove_cause(impact_type: str, cause: str) -> bool:
    """Remove a cause from an impact type."""
    catalog = get_catalog()
    if impact_type not in catalog or cause not in catalog[impact_type]:
        return False
    catalog[impact_type].remove(cause)
    _save_to_file(catalog)
    return True


def rename_cause(impact_type: str, old_cause: str, new_cause: str) -> bool:
    """Rename a cause within an impact type."""
    catalog = get_catalog()
    if impact_type not in catalog:
        return False
    causes = catalog[impact_type]
    if old_cause not in causes or new_cause in causes:
        return False
    idx = causes.index(old_cause)
    causes[idx] = new_cause
    _save_to_file(catalog)
    return True


# ======================================================================
# Utilities
# ======================================================================

def _catalog_replace(new_catalog: dict[str, list[str]]) -> None:
    """Replace the entire runtime catalog and persist."""
    global _catalog
    _catalog = new_catalog
    _save_to_file(new_catalog)


def reset_catalog() -> None:
    """Reset the runtime catalog to defaults and persist."""
    global _catalog
    _catalog = {k: list(v) for k, v in DEFAULT_IMPACT_CAUSE_CATALOG.items()}
    _save_to_file(_catalog)
