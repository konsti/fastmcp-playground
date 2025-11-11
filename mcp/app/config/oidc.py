"""
OpenID Connect configuration helpers.
"""

# import httpx
from app.config.settings import settings


# def get_oidc_config() -> dict:
#     """
#     Fetch OpenID Connect configuration from the well-known endpoint.

#     Returns:
#         dict: Configuration containing issuer, jwks_uri, authorization_endpoint, etc.

#     Raises:
#         ValueError: If OIDC configuration URL is not set
#         RuntimeError: If fetching configuration fails
#     """
#     config_url = settings.keycloak_config_url

#     if not config_url:
#         raise ValueError("KEYCLOAK_OPENID_CONFIGURATION environment variable is not set")

#     try:
#         response = httpx.get(config_url, timeout=10.0)
#         response.raise_for_status()
#         config = response.json()

#         return {
#             "config_url": config_url,
#             "issuer": config.get("issuer"),
#             "jwks_uri": config.get("jwks_uri"),
#             "authorization_endpoint": config.get("authorization_endpoint"),
#             "token_endpoint": config.get("token_endpoint"),
#             "revocation_endpoint": config.get("revocation_endpoint"),
#         }
#     except Exception as e:
#         raise RuntimeError(f"Failed to fetch OIDC configuration from {config_url}: {e}")


def get_oauth_config() -> dict:
    """
    Get OAuth configuration from environment variables.

    Returns:
        dict: Configuration containing client_id, client_secret, and base_url

    Raises:
        ValueError: If required OAuth settings are not set
    """
    client_id = settings.keycloak_client_id
    client_secret = settings.keycloak_client_secret
    base_url = settings.base_url

    if not client_id:
        raise ValueError("KEYCLOAK_CLIENT_ID environment variable is not set")
    if not client_secret:
        raise ValueError("KEYCLOAK_CLIENT_SECRET environment variable is not set")

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "base_url": base_url,
    }
