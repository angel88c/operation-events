# ============================================================================
# Configuration Module
# ============================================================================
# Centralized configuration management for the application.
# Loads settings from environment variables and provides typed access.
# ============================================================================

from config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
