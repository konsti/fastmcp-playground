"""
Configuration management module.
"""

from app.config.settings import settings
from app.config.oidc import get_oauth_config

__all__ = ["settings", "get_oauth_config"]
