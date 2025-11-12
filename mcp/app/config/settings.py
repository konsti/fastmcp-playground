"""
Application settings and environment variables.

Environment Loading Priority:
1. System environment variables (highest priority)
2. .env file (fallback if system env not set)
3. Field defaults (used if neither above is set)

Usage:
    # Default: loads from .env if present, otherwise system env vars
    from app.config.settings import settings

    # Override env file for testing:
    ENV_FILE=.env.test python main.py
"""

import os
from enum import Enum

from pydantic import Field, HttpUrl, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Application environment types."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging level options."""

    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    python_env: Environment = Field(
        default=Environment.DEVELOPMENT, description="The application environment"
    )

    log_level: LogLevel = Field(
        default=LogLevel.INFO, description="The logging level for the application"
    )

    host: str = Field(
        default="0.0.0.0", description="The host that the MCP Server will bind to"
    )

    port: int = Field(
        default=8000,
        ge=0,
        le=65535,
        description="The port that the MCP Server will listen on",
    )

    base_url: HttpUrl | None = Field(
        default=None,
        description="The base URL of the MCP Server. If not set, will be derived from host and port",
    )

    # Keycloak/OIDC settings
    keycloak_openid_configuration: HttpUrl = Field(
        description="The OpenID Connect configuration URL for Keycloak"
    )

    keycloak_client_id: str = Field(
        min_length=1, description="The client ID for Keycloak authentication"
    )

    keycloak_client_secret: str = Field(
        min_length=1, description="The client secret for Keycloak authentication"
    )

    # Portfolio API settings
    portfolio_api_url: HttpUrl = Field(
        description="The base URL for the Portfolio API service"
    )

    @model_validator(mode="after")
    def set_base_url_if_not_provided(self) -> "Settings":
        """Set base_url from host and port if not explicitly provided."""
        if self.base_url is None:
            # Use object.__setattr__ to bypass Pydantic's frozen behavior if enabled
            object.__setattr__(self, "base_url", f"http://{self.host}:{self.port}")
        return self


settings: Settings = Settings()  # pyright: ignore[reportCallIssue]
