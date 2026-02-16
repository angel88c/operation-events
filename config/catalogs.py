"""
============================================================================
Catálogos de Impacto y Causa — Operation Events
============================================================================
Catálogos configurables de Tipos de Impacto y sus Causas asociadas.
Estos catálogos se usan en la pantalla de Captura (RF-001) y se pueden
administrar desde la pantalla de Configuración (RF-004).

Referencia: specs/operation-events.md — Sección 11
============================================================================
"""

from __future__ import annotations

from typing import Any


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


def get_catalog() -> dict[str, list[str]]:
    """
    Return the current impact→cause catalog.
    On first call, initializes from DEFAULT_IMPACT_CAUSE_CATALOG.
    In the future, this can load from SharePoint or a config file.
    """
    global _catalog
    if _catalog is None:
        # Deep copy so mutations don't affect the default
        _catalog = {k: list(v) for k, v in DEFAULT_IMPACT_CAUSE_CATALOG.items()}
    return _catalog


def get_impact_types() -> list[str]:
    """Return the list of available impact types."""
    return list(get_catalog().keys())


def get_causes_for_impact(impact_type: str) -> list[str]:
    """Return the list of causes associated with a given impact type."""
    return get_catalog().get(impact_type, [])


def reset_catalog() -> None:
    """Reset the runtime catalog to defaults. Useful after config changes."""
    global _catalog
    _catalog = None
