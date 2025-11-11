"""
Authentication setup and configuration.
"""

from fastmcp.server.auth.oidc_proxy import OIDCProxy
from app.config import get_oauth_config, settings


def setup_auth() -> OIDCProxy | None:
    """
    Setup authentication provider based on configuration.
    
    Returns:
        OIDCProxy | None: Configured authentication provider
    """
    settings.validate()
    
    oauth_config = get_oauth_config()
    
    # oauth_proxy = OAuthProxy(
    #     upstream_authorization_endpoint=oidc_config["authorization_endpoint"],
    #     upstream_token_endpoint=oidc_config["token_endpoint"],
    #     upstream_client_id=oauth_config["client_id"],
    #     upstream_client_secret=oauth_config["client_secret"],
    #     upstream_revocation_endpoint=oidc_config["revocation_endpoint"],
    #     token_verifier=JWTVerifier(
    #         jwks_uri=oidc_config["jwks_uri"],
    #         issuer=oidc_config["issuer"],
    #     ),
    #     base_url=oauth_config["base_url"],
    # )
    
    # Create OIDC proxy
    oidc_proxy = OIDCProxy(
        config_url=settings.keycloak_config_url,
        client_id=oauth_config["client_id"],
        client_secret=oauth_config["client_secret"],
        base_url=oauth_config["base_url"],
    )
    
    return oidc_proxy

