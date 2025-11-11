"""
Application settings and environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Server settings
        self.server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
        self.server_port: int = int(os.getenv("SERVER_PORT", "8000"))
        self.base_url: str = os.getenv("SERVER_BASE_URL", f"http://localhost:{self.server_port}")
        
        # Keycloak/OIDC settings
        self.keycloak_config_url: str | None = os.getenv("KEYCLOAK_OPENID_CONFIGURATION")
        self.keycloak_client_id: str | None = os.getenv("KEYCLOAK_CLIENT_ID")
        self.keycloak_client_secret: str | None = os.getenv("KEYCLOAK_CLIENT_SECRET")
        
    def validate(self):
        """Validate required settings."""
        if not self.keycloak_config_url:
            raise ValueError("KEYCLOAK_OPENID_CONFIGURATION environment variable is required when auth is enabled")
        if not self.keycloak_client_id:
            raise ValueError("KEYCLOAK_CLIENT_ID environment variable is required when auth is enabled")
        if not self.keycloak_client_secret:
            raise ValueError("KEYCLOAK_CLIENT_SECRET environment variable is required when auth is enabled")


# Global settings instance
settings = Settings()
