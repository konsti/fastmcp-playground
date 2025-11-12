"""
Authentication setup and configuration.
"""

from fastmcp.server.auth.oidc_proxy import OIDCProxy
from app.config import settings


def setup_auth() -> OIDCProxy | None:
    """
    Setup authentication provider based on configuration.

    Returns:
        OIDCProxy | None: Configured authentication provider
    """

    oidc_proxy = OIDCProxy(
        config_url=str(settings.keycloak_openid_configuration),
        client_id=settings.keycloak_client_id,
        client_secret=settings.keycloak_client_secret,
        base_url=str(settings.base_url),
    )

    return oidc_proxy
