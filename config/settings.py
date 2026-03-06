"""
============================================================================
Application Settings
============================================================================
Centralized configuration using Pydantic for validation.
Loads from .env file and environment variables.
============================================================================
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All settings can be overridden via .env file or system env vars.
    """

    # --- Azure AD / Microsoft 365 ---
    azure_client_id: str = Field(default="", description="Azure AD Application (client) ID")
    azure_client_secret: str = Field(default="", description="Azure AD Client Secret")
    azure_tenant_id: str = Field(default="", description="Azure AD Tenant ID")
    azure_redirect_uri: str = Field(
        default="http://localhost:8501",
        description="OAuth2 redirect URI",
    )

    # --- SharePoint / Microsoft Lists ---
    sharepoint_site_id: str = Field(default="", description="SharePoint Site ID for Microsoft Lists")
    sharepoint_list_id: str = Field(default="", description="SharePoint List ID for events storage")
    sharepoint_domain: str = Field(default="", description="SharePoint domain (e.g. contoso.sharepoint.com)")
    user_domain: str = Field(default="ibtest.com", description="Email domain filter for user selectors (e.g. ibtest.com)")

    # --- Email Notifications ---
    email_sender: str = Field(default="", description="Email address to send notifications from (must have Send.Mail permission)")
    app_url: str = Field(default="http://localhost:3001", description="App URL for email links")

    # --- Application ---
    app_name: str = Field(default="Operation Events", description="Application display name")
    app_description: str = Field(default="Captura y análisis de eventos operativos en producción", description="Short app description for login page")
    app_version: str = Field(default="1.0.0", description="Application version")
    app_env: str = Field(default="development", description="Environment: development | staging | production")

    # --- Feature Flags ---
    enable_auth: bool = Field(default=True, description="Enable Microsoft 365 authentication")
    enable_debug: bool = Field(default=False, description="Enable debug mode with extra logging")

    class Config:
        env_file = str(ROOT_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def azure_authority(self) -> str:
        """Microsoft identity platform authority URL."""
        if self.azure_tenant_id:
            return f"https://login.microsoftonline.com/{self.azure_tenant_id}"
        return "https://login.microsoftonline.com/common"

    @property
    def azure_scopes(self) -> list[str]:
        """Default Microsoft Graph API scopes.
        Note: Do NOT include reserved OIDC scopes (openid, profile, offline_access)
        — MSAL adds them automatically.
        """
        return ["User.Read"]

    @property
    def graph_app_scopes(self) -> list[str]:
        """Scopes for application-level (client credentials) Graph API calls."""
        return ["https://graph.microsoft.com/.default"]


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached singleton instance of Settings.
    Call this instead of instantiating Settings directly.
    """
    return Settings()
